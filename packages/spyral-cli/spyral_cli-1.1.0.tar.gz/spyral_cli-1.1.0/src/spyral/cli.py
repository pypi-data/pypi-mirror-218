from typing import List, IO, Optional
import subprocess as sp
import sys
import re
from datetime import datetime
from pathlib import Path
import time
import threading
import csv
import platform

if sys.version_info >= (3, 11):
    from enum import StrEnum
else:
    from backports.strenum import StrEnum

import typer
import psutil
import rich.live
import rich.text
import rich.console
import rich.panel
import rich.rule
import plotext

app = typer.Typer(rich_markup_mode="rich")


class Monitor:
    interval: float

    max_rss: float = 0
    max_vms: float = 0

    terminate: bool = False

    exception = None

    def __init__(
        self,
        command: List[str],
        output: IO[str],
        interval: float = 0.5,
        live: Optional[rich.live.Live] = None,
    ):
        self.interval = interval
        self.live = live
        self.command = command
        self.writer = csv.writer(output)
        self.writer.writerow(("time", "rss", "vms"))

        self.time: List[float] = [0]
        self.rss: List[float] = [0]
        self.vms: List[float] = [0]

    def run(self, p: psutil.Process):
        try:
            start = datetime.now()
            while p.is_running() and p.status() in (
                psutil.STATUS_RUNNING,
                psutil.STATUS_SLEEPING,
            ):
                if self.terminate:
                    return
                delta = (datetime.now() - start).total_seconds()
                rss = p.memory_info().rss
                vms = p.memory_info().vms
                for subp in p.children(recursive=True):
                    try:
                        rss += subp.memory_info().rss
                        vms += subp.memory_info().vms
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        pass

                self.rss.append(rss / 1e6)
                self.vms.append(vms / 1e6)
                self.time.append(delta)
                self.max_rss = max(rss, self.max_rss)
                self.max_vms = max(vms, self.max_vms)

                self.writer.writerow((delta, rss, vms))

                if self.live is not None:
                    self.live.update(
                        rich.console.Group(
                            rich.rule.Rule("Memory monitoring"),
                            rich.text.Text("Running: " + " ".join(self.command)),
                            rich.text.Text(
                                f"[{delta:8.2f}s] [rss: {rss/1e6:8.2f}M, max: {self.max_rss/1e6:8.2f}M] [vms: {vms/1e6:8.2f}M, max: {self.max_vms/1e6:8.2f}M]"
                            ),
                        )
                    )

                time.sleep(self.interval)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return
        except Exception as e:
            self.exception = e
            raise e


@app.command()
def run(
    cmd: List[str],
    interval: float = typer.Option(0.5, "--interval", "-i"),
    output: Path = typer.Option("spyral.csv", "--output", "-o"),
    summary: bool = sys.stdout.isatty(),
    label: Optional[str] = typer.Option(None, "--label", "-l"),
):
    p = psutil.Popen(cmd, stdout=sp.PIPE, stderr=sp.STDOUT)
    console = rich.console.Console()

    with rich.live.Live(console=console, transient=not summary) as live, output.open(
        "w"
    ) as ofh:
        ofh.write("# spyral-cmd: " + " ".join(cmd) + "\n")
        if label is not None:
            ofh.write("# spyral-label: " + label + "\n")
        mon = Monitor(interval=interval, live=live, output=ofh, command=cmd)
        t = threading.Thread(target=mon.run, args=(p,))
        t.start()

        try:
            while p.is_running() and p.status() in (
                psutil.STATUS_RUNNING,
                psutil.STATUS_SLEEPING,
            ):
                for line in iter(p.stdout.readline, b""):
                    if not t.is_alive() and mon.exception is not None:
                        print("Monitoring thread has died")
                        print("Exception:", str(mon.exception))
                        raise RuntimeError("Monitoring thread has died")
                    live.console.out(line.decode("utf-8"), highlight=False, end="")
        except KeyboardInterrupt:
            mon.terminate = True
            t.join()
            p.kill()
            raise

        p.wait()
        t.join()

    if summary:
        console.rule("Memory usage")
        plotext.clf()

        plotext.plot_size(
            plotext.terminal_width(), max(10, (plotext.terminal_height() or 70) / 3)
        )

        plotext.xlabel("time [s]")
        plotext.ylabel("memory [M]")

        plotext.plot(mon.time, mon.rss, label="rss")
        if platform.system() == "Darwin":
            plotext.plot(mon.time, [v / 1000 for v in mon.vms], label="vms * 10^3")
        else:
            plotext.plot(mon.time, mon.vms, label="vms")

        plotext.show()  # to finally plot


class Format(StrEnum):
    pdf = "pdf"
    png = "png"


@app.command()
def plot(
    csv: Path = typer.Argument(..., dir_okay=False, exists=True),
    formats: List[Format] = ["pdf"],
    output: Path = typer.Option(
        Path.cwd(), "--output", "-o", file_okay=False, exists=True
    ),
):
    console = rich.console.Console()
    with console.status("Importing plotting modules"):
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import pandas as pd

    df = pd.read_csv(csv, comment="#")
    df.rss /= 1e6
    df.vms /= 1e6
    fig, ax = plt.subplots()
    df.plot("time", y="rss", ax=ax, c="tab:orange")
    df.plot("time", y="vms", ax=ax, c="tab:blue")

    rss_imax = df.rss.argmax()
    ax.axvline(df.time.iloc[rss_imax], ls="--", c="tab:orange")
    ax.axhline(df.rss.iloc[rss_imax], ls="--", c="tab:orange")

    vms_imax = df.vms.argmax()
    ax.axvline(df.time.iloc[vms_imax], ls="--", c="tab:blue")
    ax.axhline(df.vms.iloc[vms_imax], ls="--", c="tab:blue")

    ax.set(xlabel="time [s]", ylabel="memory [M]")

    fig.tight_layout()
    for f in formats:
        fig.savefig(output / f"{csv.stem}.{f.name}")


@app.command()
def maxima(
    output: Path = typer.Argument(..., dir_okay=False),
    inputs: List[Path] = typer.Argument(...),
    extra_columns: List[str] = typer.Option([], "--extra-column", "-e"),
):
    import pandas as pd

    with output.open("a") as fh:
        writer = csv.writer(fh)

        for i in inputs:
            cmd = None
            label = None
            with i.open("r") as ifh:
                for _, line in zip(range(10), ifh):
                    if m := re.match(r" *# spyral-cmd: (.*)", line):
                        cmd = m.group(1).strip()
                    if m := re.match(r" *# spyral-label: (.*)", line):
                        label = m.group(1).strip()
                        break
            assert cmd or label
            if label is None:
                label = cmd

            df = pd.read_csv(i, comment="#")
            writer.writerow(
                extra_columns + [label, df.time.iloc[-1], df.rss.max(), df.vms.max()]
            )
