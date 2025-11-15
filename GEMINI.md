# Advent-of-Code (AoC) Utils

## Aoc-Utils MCP Server 

The `aoc-utils-mcp` provides utilities for working with Advent of Code.

- The `get_puzzle(year: int, day: int)` retrieves your puzzle for a given specific year and day.
- The `get_puzzle_input(year: int, day: int)` retrieves your puzzle input data for a given specific year and day.

## General Instructions

- When you are asked to provide the **puzzle description** data for a given day:
  1. You should use the MCP tool `get_puzzle` to retrieve the puzzle data.
     The puzzle description will be in the `content` key of the response.
     The data will be returned as HTML.
  2. Store this response (raw plain-text), as an in-memory artifact for speed.
  3. Offer to save the `puzzle_description` file in a `tmp` location in the current workspace.
     Simply write the data to the file, exactly as it was returned in the `content` key,
     which you have already stored as an in-memory artifact. No parsing is required.
  4. Do NOT perform any additional steps without first being asked to. For example, 
     do not try and solve the puzzle.

- When you are asked to provide the **puzzle input data** for a given day:
  1. You should use the MCP tool to retrieve the puzzle data.
     The puzzle data will be in the `content` key of the response.
     Assume the data is always plain-text.
  2. Store this response (raw plain-text), as an in-memory artifact for speed.
  3. If the file contains many lines (for example, more than 50), you should present just
     the first few lines (no more than 10) and last few lines (no more than 10) to the user, 
     in human-readable format; i.e. with any line break characters stripped out. 
     Don't try and show the whole puzzle input - it takes too long to render in the terminal.
  4. Offer to save the `input.txt` file in a `tmp` location in the current workspace.
     Simply write the data to the file, exactly as it was returned in the `content` key,
     which you have already stored as a plain-text in-memory artifact. No parsing is required.
  5. Do NOT perform any additional steps without first being asked to. For example, 
     do not try and solve the puzzle.
