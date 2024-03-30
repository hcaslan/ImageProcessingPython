# Image Processing with Python

This README.md file provides an overview of the Object-Oriented Programming II Lab Final Report for the 2021-2022 Spring Semesters.

## Overview

The program consists of a graphical user interface (GUI) with a menu bar and three main headers. The headers include the 'source' header, where a source file can be imported and basic operations can be performed on it. The 'operations' header contains the main features of the program, allowing changes to be made to the imported source file. The 'output' header displays the final version of the modified source file and provides some simple actions.

## Getting Started

To run the program, simply execute it. Upon launching, you will see a screen with a menu bar and limited functionality. Only the exit and open-source buttons will be available initially.

## Source Header

The 'source' header allows you to select the source file and perform operations on it. By clicking the 'open source' button, you can choose the desired file. Once a source file is selected, additional buttons such as 'Export as' and 'Clear' become available. The 'Export as' button enables saving the source file with a different extension, while the 'Clear' button deletes the source file.

## Operations Header

Under the 'operations' header, you can find various buttons and sub-headers for performing operations on the source file. These operations include 'undo', 'redo', 'clear all', conversion, segmentation, and edge detection. Please note that certain operations may display warnings if the selected image is not suitable for the operation.

## Output Header

The 'output' header displays the result of the performed operations on the source file. After any operation is executed, the result is shown under this header. The buttons under the 'output' header allow you to perform actions on the output image, such as saving, exporting, and clearing.

## Menubar

The menu bar provides access to all available operations and their corresponding shortcut keys. It reflects the operations that can be performed at any given time.

## Implementation Details

The program implements features such as undo and redo functionality, check for repetitive operations, and prompting the user before exiting. The undo and redo buttons allow you to revert or repeat previous operations. Repetitive operations are blocked to avoid redundant results. When exiting the application, it will prompt the user to save if any operations have been performed on the source file.

## Usage

1. Run the program.
2. Use the menu bar or headers to perform desired operations on the source file.
3. Review the output under the 'output' header.
4. Save, export, or clear the output image as needed.
5. Exit the application, with the option to save if necessary.

This README.md file provides a brief overview of the program and its functionalities. For more detailed information, refer to the full Lab Final Report.

## License

This program is licensed under the [MIT License](https://opensource.org/licenses/MIT).
