from typing import Optional, Union
from ctypes import c_char

import numpy

def from_ansi_output(ansi_output: str):
    """
    Make a Discord coloured message from ANSI output.
    NOTE: This function is a bare bones minimum, which just formats the string as a code block.
          This package has better tools for creating Discord ANSI messages, but basic functionality
          like this one is still included. If you want to easily create ANSI messages, for example, help command
          for your bot and you don't have existing output from terminal, please use other tools present in this library.
    For example, you run `ls --color=always` and you want to send output to Discord, saving the colour.
    You can call this function with the output from the `ls` command to get the coloured message.
    Or, you want to send the logs for your bot to a channel, and it has color in it. Colorama works too with this function!
    Again, this function is made for formatting the already existing terminal output to be sent in Discord. If you want to
    create your own message, use other tools present in this library.

    Parameters
    ----------
    ansi_output: str | required
        The output from the terminal command.
    """
    return "```ansi\n" + ansi_output + "\n```"


background_colors = {
    'black': 40,
    'orange': 41,
    'gray-1': 42,
    'gray-2': 43,
    'gray-3': 44,
    'blue': 45,
    'gray-4': 46,
    'white': 47
}

foreground_colors = {
    'black': 30,
    'red': 31,
    'green': 32,
    'yellow': 33,
    'blue': 34,
    'magenta': 35,
    'cyan': 36,
    'white': 37
}

class MessageBuilder:
    indentLevel: int
    output: list
    indentSize: int
    
    def __init__(self):
        self.indentLevel = 0
        self.output = []
        self.indentSize = 4
    
    def setIndentationSize(self, indentSize: int):
        """
        Set indentation size (4 by default)
        """
        self.indentSize = indentSize
    
    def getText(self):
        """
        Get the resulting message
        """
        return "```ansi\n" + '\n'.join(self.output) + "\n```"
    
    def addNewline(self):
        """
        Insert a new line
        """
        self.output.append(" " * self.indentSize * self.indentLevel)
    
    def insertANSIText(self, ansiText: str, reset_style_before_text: bool = True, reset_style_after_text: bool = True):
        """
        Insert some ANSI text.
        
        Parameters
        ----------
        ansiText : str | required
            The text you want to insert.
        reset_style_before_text : bool | optional
            Reset the style and color before inserting the text.
        reset_style_before_text : bool | optional
            Reset the style and color after inserting the text.
        """
        splittedText = ansiText.split("\n")
        if self.output[-1] == "" or self.output[-1].replace("\033[0m", "").strip() == "":
            self.output[-1] = " " * self.indentSize * self.indentLevel
        if reset_style_before_text:
            self.output[-1] += "\033[0m"
        for x in splittedText:
            if self.output[-1] == "":
                self.output[-1] = " " * self.indentSize * self.indentLevel
            else:
                self.output.append(" " * self.indentSize * self.indentLevel)
            self.output[-1] += x
        if reset_style_after_text:
            self.output[-1] += "\033[0m"
    
    def addText(self, text: str, background: Optional[str] = None, foreground: Optional[str] = None, reset_style_before_text: bool = True, reset_style_after_text: bool = True, bold: bool = False, underlined: bool = False):
        """
        Add a piece of text. It will not let you insert ANSI text, it escapes the \033 character.
        To insert a piece of ANSI formatted text, use the insertANSIText(ansiText) function
        
        Too much parameters, I won't type out the description here for all of them.
        """
        if len(self.output) == 0:
            self.output.append("")
        splittedText = text.replace("\033", "\\033").split("\n")
        if self.output[-1] == "" or self.output[-1].replace("\033[0m", "").strip() == "":
            self.output[-1] = " " * self.indentSize * self.indentLevel
        if reset_style_before_text:
            self.output[-1] += "\033[0m"
        firstIteration = True
        for x in splittedText:
            if self.output[-1].replace("\033[0m", "").replace(" ", "") == "":
                self.output[-1] = "\033[0m" + (" " * self.indentSize * self.indentLevel)
            elif not firstIteration:
                self.output.append("\033[0m" + (" " * self.indentSize * self.indentLevel))
            if background:
                self.output[-1] += f"\033[{background_colors[background]}m"
            if foreground:
                self.output[-1] += f"\033[{foreground_colors[foreground]}m"
            if bold:
                self.output[-1] += "\033[1m"
            if underlined:
                self.output[-1] += "\033[4m"
            self.output[-1] += x
            firstIteration = False
        if reset_style_after_text:
            self.output[-1] += "\033[0m"

class ANSIArt:
    data: list
    size: tuple
    
    def __init__(self, sizex: int, sizey: int):
        self.size = (sizex, sizey)
        self.data = numpy.full(self.size, "white", dtype='U7')
    
    def getPixel(self, x: int, y: int):
        """
        Gets the color of a pixel.
        Please note that it starts counting from 0.
        
        Parameters
        ----------
        x : int | required
            X position
        y : int | required
            Y position
        """
        return self.data[x][y][0]
    
    def setPixel(self, x: int, y: int, color: str):
        """
        Sets the color of a pixel.
        Please note that it starts counting from 0.
        
        Parameters
        ----------
        x : int | required
            X position
        y : int | required
            Y position
        color : str | required
            A valid color
        """
        if color not in background_colors:
            raise Exception("Invalid background color! (You can only use background colors, not foreground ones!)")
        self.data[x][y][0] = color
    
    def getPixelTextColor(self, x: int, y: int):
        """
        Gets the color of the text inside of a pixel.
        Please note that it starts counting from 0.
        
        Parameters
        ----------
        x : int | required
            X position
        y : int | required
            Y position
        """
        return self.data[x][y][1]
    
    def setPixelTextColor(self, x: int, y: int, color: str):
        """
        Sets the color of the text inside of a pixel.
        Please note that it starts counting from 0.
        
        Parameters
        ----------
        x : int | required
            X position
        y : int | required
            Y position
        color : str | required
            A valid color
        """
        if color not in background_colors:
            raise Exception("Invalid foreground color! (You can only use foreground colors for character colors!)")
        self.data[x][y][1] = color
    
    def setPixelChar(self, x: int, y: int, char: Union[str, c_char]):
        """
        Set a character to be inside the pixel.
        
        Parameters
        ----------
        x : int | required
            X position
        y : int | required
            Y position
        char : Union[str, c_char] | required
            The character you want to put there
        """
        if type(char) == c_char:
            char = chr(char.value[0])
        if len(char) != 1:
            raise Exception("Must be one character!")
        self.data[x][y][2] = char
    
    def fillSquare(self, x1: int, y1: int, x2: int, y2: int, color: str):
        """
        Makes a square, from (x1, y1) to (x2, y2) inclusive!
        Please note that it starts counting from 0.
        
        Parameters
        ----------
        x1 : int | required
            Starting X position
        y1 : int | required
            Starting Y position
        x2 : int | required
            Ending X position (inclusive)
        y2 : int | required
            Ending Y position (inclusive)
        """
        for y in range(y1, y2 + 1):
            for x in range(x1, x2 + 1):
                self.data[x][y] = color
    
    def fillAll(self, color: str):
        """
        Fill the entire image with a color.
        
        Parameters
        ----------
        color : str | required
            The color to fill the image with.
        """
        self.fillSquare(0, 0, self.size[0] - 1, self.size[1] - 1, color)
            
    
    def render(self):
        """
        Render this image.
        """
        
        data = "```ansi\n\033[0m"
        current_color = ""
        for x in self.data:
            for color in x:
                if color != current_color:
                    data += f"\033[{background_colors[color]}m"
                    current_color = color
                data += "  "
            data += "\n"
        data += "```"
        return data
