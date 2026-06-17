from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

from weather_tool import get_destination_weather
from planner_agent import generate_itinerary
from utils import parse_trip_days

console = Console()


def main():
    console.print(Panel.fit(
        "[bold cyan]AI Travel Planner Agent[/bold cyan]\n"
        "Weather-based itinerary and packing assistant",
        border_style="cyan"
    ))

    destination = Prompt.ask("Where are you planning to travel?")
    days_text = Prompt.ask(
        "How many days do you want to plan? OpenWeather supports the next 5 days",
        default="5"
    )
    budget_type = Prompt.ask(
        "Budget type",
        choices=["low", "medium", "high"],
        default="medium"
    )

    try:
        trip_days = parse_trip_days(days_text)

        console.print("\n[cyan]Calling Weather Tool...[/cyan]")
        weather_data = get_destination_weather(destination, days_limit=trip_days)

        console.print("[green]Weather data received.[/green]")
        console.print("[cyan]Generating AI itinerary with Ollama...[/cyan]\n")

        itinerary = generate_itinerary(
            weather_data=weather_data,
            budget_type=budget_type
        )

        console.print(Panel(
            itinerary,
            title="[bold green]Your AI Travel Plan[/bold green]",
            border_style="green"
        ))

    except Exception as error:
        console.print(f"[bold red]Error:[/bold red] {error}")


if __name__ == "__main__":
    main()
