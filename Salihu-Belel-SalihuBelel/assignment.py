import os
import time
from datetime import datetime, timedelta

class DuplicateVisitorError(Exception):
    pass

class TooSoonError(Exception):
    pass


def log_visitor(filename="visitors.txt"):
    visitor_name = input("Enter visitor's name: ").strip()

    if not os.path.exists(filename):
        with open(filename, "w") as f:
            f.write("")  

    last_name, last_time = None, None
    with open(filename, "r") as f:
        lines = f.readlines()
        if lines:
            last_line = lines[-1].strip()
            parts = last_line.split(" | ")
            if len(parts) == 2:
                last_name, last_time_str = parts
                last_time = datetime.strptime(last_time_str, "%Y-%m-%d %H:%M:%S")


    if visitor_name == last_name:
        raise DuplicateVisitorError(f"Visitor '{visitor_name}' already entered last time!")


    if last_time and datetime.now() - last_time < timedelta(minutes=5):
        raise TooSoonError("Another visitor cannot enter until 5 minutes have passed.")


    with open(filename, "a") as f:
        f.write(f"{visitor_name} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    print(f"Visitor {visitor_name} logged successfully!")


if __name__ == "__main__":
    try:
        log_visitor()
    except DuplicateVisitorError as e:
        print("Error:", e)
    except TooSoonError as e:
        print("Error:", e)
    except Exception as e:
        print("Unexpected Error:", e)
