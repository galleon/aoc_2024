Trying to solve the AoC puzzle using LLMs.


## Prompts

### Part 1

```
You are an expert at solving puzzles using python 3.10. You pay a specific attention to improvements to reduce the search space and speed up calculations.
You will be given a puzzle description from which you will generate some code to solve it. You will also extract the example input and outputs.
THe output will be a JSON structure with the following format:
{
    "code": "your code",
    "example_input": "example input",
    "example_output": "example output"
}

The code will be made of several parts:
  - one read_data function will read the input file 'input.txt'and returns a data structure
  - the part1 function will take this data structure as parameter and return the result
  - main will print the result

Here is the description of the puzzle:
```

### Part 2

```
Here is part 2.
Part 2 is a continuation of part1 but it usually requires specific improvements to reduce the search space and speed up calculations. For example, you might have to reduce space search and use vectorized operations.
Add a function named part2.

The puzzle is below:
```

## Results

|  Day  | Part  | GPT-o1 | Claude 3.5 Sonnet | Gemini 2.0 Flash |
| :---: | :---: | :----: | :---------------: | :--------------: |
|  18   |   1   |   👍    |         👍         |        👎         |
|       |   2   |   👍    |         👍         |        👎         |
|  19   |   1   |   👍    |         👎         |        👎         |
|       |   2   |   👍    |         👎         |        👎         |
|  20   |   1   |   👍    |         👎         |        👎         |
|       |   2   |   👍    |         👎         |        👎         |
|  21   |   1   |   👎    |         👎         |        👎         |
|       |   2   |   👎    |         👎         |        👎         |
|  22   |   1   |   👍    |         👍         |        👍         |
|       |   2   |   👍    |         👎         |        👎         |
|  23   |   1   |   👍    |         👍         |        👍         |
|       |   2   |   👍    |         👎         |        👎         |
|  24   |   1   |   👍    |         👎         |        👎         |
|       |   2   |   👎    |         👎         |        👎         |
|  25   |   1   |   👍    |         👎         |        👎         |
|       |       | 11/15  |       4/15        |       2/15       |
