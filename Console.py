from visualization import VisualizationTool

from rich import print
from devices import Devices

import msvcrt

class Console_():
    def start_menu(self):

        self.print_introduction()

        command = input('\nEnter a command or command number: ')

        self.commands(command.lower())

    def print_introduction(self):
        print(f'\n[red]Hello![/red] This is a program that collects all information about [i]button clicks.[/i]\n'
        'Here is the [bold green]command list[/bold green]:\n'
        '\n[bold green][------------------------Command list------------------------] [/bold green]\n\n'
        '[bold sea_green3]#[/bold sea_green3] 1. [red]start[/red]\n'
        'The command that starts recording keystrokes\n\n'
        '[bold sea_green3]#[/bold sea_green3] 2. [red]click_area[/red]\n'
        'Shows where you clicked on the screen\n\n'
        '[bold sea_green3]#[/bold sea_green3] 3. [red]mouse_stats[/red]\n'
        'Shows the number of mouse clicks\n\n'
        '[bold sea_green3]#[/bold sea_green3] 4. [red]keyboard_stats[/red]\n'
        'Shows the number of keystrokes\n\n'
        '[bold sea_green3]#[/bold sea_green3] 5. [red]clicks_per_day[/red]\n'
        'Shows the number of clicks made in N-day\n\n'
        '[bold sea_green3]#[/bold sea_green3] 6. [red]clicks_per_hour[/red]\n'
        'Shows the number of clicks made per hour for the entire time.\n\n'
        '[bold sea_green3]#[/bold sea_green3] 7. [red]top_50_keys[/red]\n'
        'Shows the fifty most popular keystrokes as a bar.\n\n'
        '[bold sea_green3]#[/bold sea_green3] 8. [red]exit[/red]\n'
        'Indeed')

    def commands(self, command):
        visual_tool = VisualizationTool()
        match command:
            case 'start' | '1':
                print("[bold]The program has started! If you want to exit, use F12")
                devices = Devices()
                devices.start_listeners()  
            case 'click_area' | '2':
                visual_tool.area_of_clicking()
            case 'mouse_stats' | '3':
                visual_tool.stats_of_mouse()
            case 'keyboard_stats' | '4':
                visual_tool.stats_of_keyboard()
            case 'clicks_per_day' | '5':
                visual_tool.clicks_per_day()
            case 'clicks_per_hour' | '6':
                visual_tool.clicks_per_hour()
            case 'clicks_per_hour' | '7':
                visual_tool.show_top_50_keys()
            case 'exit' | '8':
                exit()
            case _ : 
                print('[bold red]\n\nInvalid Command[/bold red]')
            
        print("\n\nPress any key to continue...")
        msvcrt.getch()

        self.start_menu()

if __name__ == '__main__':
    console = Console_() 
    console.start_menu()