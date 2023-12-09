"""
Advent of code challenge 2022

Not really competetive with time today, spread coding over multiple sessions
Start  - 18:09 
Part 1 - 19:58 - 1350966
Part 2 - 20:34 - 6296435
"""


class FileFolder:
    """
    Can store either a file or a folder.
    """

    def __init__(self, isdir: bool, name: str, size: int = None) -> None:
        self.name, self.isdir, self.file_size = name, isdir, size
        if isdir:
            self.content = []
    
    def add_to_folder(self, other) -> None:
        self.content.append(other)
    
    @property
    def size(self) -> int:
        if self.isdir:
            return sum([item.size for item in self.content])
        else:
            return int(self.file_size)

    def __str__(self) -> str:
        """Generates a readeable string in the same format as used in the example."""
        if not self.isdir:
            return '- {} (file, size = {})'.format(self.name, self.size)
        else:
            # return '- {} (dir)\n  '.format(self.name) + \
            return '- {} (dir, size = {})\n  '.format(self.name, self.size) + \
                '\n  '.join('\n'.join([str(item) for item in self.content]).split('\n'))
    
    def __repr__(self) -> str:
        return '<FileFolder, "{}" {}>'.format(self.name, '(dir)' if self.isdir else '(file)')
    
    def get_dirs(self) -> list:
        """Returns a list containing the current directory and all subdirectories."""
        return [self] + sum([item.get_dirs() for item in self.content if item.isdir], [])


def process_input(input_lines):
    """
    General workflow:
     - Iterate over commands
     - stack is a list keeping track of the current path. The first element is always the root 
     folder and the last element the current folder.
     - the '$ cd ' commands only change the stack and if necessary create an empty folder object. 
     Newly created folders are also added to the current folder.
     - the '$ ls' command iterates through lines and stores the items in the current folder.
    """
    root = FileFolder(True, '/')
    stack = [root]
    idx = 0
    while idx < len(input_lines):
        if input_lines[idx] == '$ cd /':
            stack = [root]
        elif input_lines[idx] == '$ cd ..':
            stack.pop()
        elif input_lines[idx].startswith('$ cd '):
            new_folder = FileFolder(True, input_lines[idx][5:])
            stack[-1].add_to_folder(new_folder)
            stack.append(new_folder)
        elif input_lines[idx] == '$ ls':
            while idx < len(input_lines) - 1:
                if input_lines[idx+1][0] == '$':
                    break
                elif input_lines[idx+1][:4] == 'dir ':
                    idx += 1
                else:
                    stack[-1].add_to_folder(FileFolder(False, *input_lines[idx + 1].split()[::-1]))
                    idx += 1
        idx += 1
    return root


if __name__ == '__main__':
    """Executed if file is executed but not if file is imported."""
    root = process_input(open('input.txt').read().split('\n'))
    print(root)
    all_dirs = root.get_dirs()

    # Part 1: Find all of the directories with a total size of at most 100000. What is the sum of 
    # the total sizes of those directories?
    print('Part 1:', sum([dir.size for dir in all_dirs if dir.size <= 100000]))

    # Part 2: Find the smallest directory that, if deleted, would free up enough space on the 
    # filesystem to run the update. What is the total size of that directory?
    # The total disk space available to the filesystem is 70000000. To run the update, you need 
    # unused space of at least 30000000. You need to find a directory you can delete that will free 
    # up enough space to run the update.
    required_space = 30000000 - (70000000 - root.size)
    print('Part 2:', min([item.size for item in all_dirs if item.size >= required_space]))
    


