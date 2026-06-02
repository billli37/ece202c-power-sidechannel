# sidechannel_agent/report.py
from datetime import datetime

def generate_iteration_report(hypothesis_mode: str, tool_output: str, iteration_count: int) -> str:
    """Formats an advanced intermediate audit report for the Human Director."""
    sep = "═" * 84
    thin = "─" * 84
    
    lines = [
        "",
        sep,
        f" SIDE-CHANNEL ANALYSIS TELEMETRY PANEL (ROUND #{iteration_count})",
        sep,
        f" Telemetry Timestamp : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f" Active Attack Mode   : {hypothesis_mode.upper()}",
        thin,
        " HISTORICAL RECOVERY RUN LOGS:",
        tool_output,
        thin,
        " USER INTERVENTION GATEWAY ACTIONS REQUIRED:",
        " • To manually force parameter modifications, submit guidance instructions below.",
        " • To allow the Agentic Loop to autonomously recalibrate and proceed, press [ENTER].",
        sep,
        ""
    ]
    return "\n".join(lines)