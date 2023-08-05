Uses ansi terminal characters to print braille barcodes.
Simple library that uses the braille unicode characters to make 4 individual barcodes in one line of text.

Installation
No dependencies, just run the braille-test.py file.

Make sure you switch terminal emulation on to allow ansi characters.


Howto:
There are two classes, the Manager to keep track of the progress bars and the Bar class to create the individual bars.

```# Create progress bar manager
    manager = ProgressBarManager()

    # Keep track of time
    start_time = time.time()

    # progress bar unique index
    bar_index = 1

    # Update and display progress bars
    while len(manager.bars) > 0 or bar_index < 15:
        # Add a new progress bar set every 3 seconds
        if time.time() - start_time > 1.3 and bar_index < 15:
            manager.add_progress_bar(f"PDF {bar_index}")
            start_time = time.time()
            bar_index += 1

        # Update progress bars
        for title in list(manager.bars.keys()):
            for index in range(4):
                increment = random.random() * 0.03
                manager.update_progress_bar(title, index, increment)

        # Remove and reposition completed progress bar sets
        for title, bar in list(manager.bars.items()):
            if all(progress >= 1 for progress in bar.progresses):
                manager.reposition_progress_bars(title)

        # Sleep before next update
        time.sleep(0.05)```