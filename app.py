import os, time, base64,io
import matplotlib
matplotlib.use("Agg")  
import matplotlib.pyplot as plt


def fcfs (head,requests):
    sequence = []
    movement = 0
    current = head
    
    for request in requests:
        sequence.append(request)
        movement = movement + abs(current-request)
        current = request
        
    return sequence,movement

def sstf(head,requests):
    
    remainings = requests[:]
    sequence = []
    movement = 0
    current = head
    
    while remainings:
        distances = []
        for remaining in remainings:
            distances.append(abs(remaining-current))
            
        shortestDistance = min(distances)
        index = distances.index(shortestDistance)
        nearest = remainings[index]
        
        sequence.append(nearest)
        movement = movement + abs(current-nearest)
        current = nearest
        
        remainings.remove(nearest)    
          
    return sequence,movement

def scan(head,requests,disk_size,direction):
    
    left = []
    right = []
    
    for request in requests:
        if request<head:
            left.append(request)
        else:
            right.append(request)
            
    left.sort()
    right.sort()
    
    sequence = []
    movement = 0
    current = head
    
    if direction == "left":
#(left) is sorted small → big.
#reversed(left) makes it big → small, so we go left correctly.
#Example left = [10, 20, 50]
#reversed = [50, 20, 10]
        for request in reversed(left):
            sequence.append(request)
            movement = movement + abs(current-request)
            current = request
            
        movement = movement + abs(current - 0)
        current = 0
        
        for request in right:
            sequence.append(request)
            movement = movement + abs(current-request)
            current = request
            
    else :
        for request in right:
            sequence.append(request)
            movement = movement + abs(current-request)
            current = request
            
        movement = movement + abs(current - (disk_size-1))
        current = disk_size-1
        
        for request in reversed(left):
            sequence.append(request)
            movement = movement + abs(current-request)
            current = request
            
    return sequence,movement

def cscan(head,requests,disk_size,direction):
    
    left = []
    right = []
    
    for request in requests:
        if request<head:
            left.append(request)
        else:
            right.append(request)
            
    left.sort()
    right.sort()
    
    sequence = []
    movement = 0
    current = head
    
    if direction == "left":
        for request in reversed(left):
            sequence.append(request)
            movement = movement + abs(current-request)
            current = request
            
        movement = movement + abs(current - 0)
        current = 0
        movement = movement + abs(current - (disk_size-1))
        current = disk_size-1
        
        for request in reversed(right):
            sequence.append(request)
            movement = movement + abs(current-request)
            current = request
            
    else :
        for request in right:
            sequence.append(request)
            movement = movement + abs(current-request)
            current = request
            
        movement = movement + abs(current - (disk_size-1))
        current = disk_size-1
        movement = movement + abs(current - 0)
        current = 0
        
        for request in left:
            sequence.append(request)
            movement = movement + abs(current-request)
            current = request
            
    return sequence,movement 
def look(head,requests,direction):
    
    left = []
    right = []
    
    for request in requests:
        if request<head:
            left.append(request)
        else:
            right.append(request)
            
    left.sort()
    right.sort()
    
    sequence = []
    movement = 0
    current = head
    
    if direction == "left":
    
        for request in reversed(left):
            sequence.append(request)
            movement = movement + abs(current-request)
            current = request
        
        for request in right:
            sequence.append(request)
            movement = movement + abs(current-request)
            current = request
            
    else :
        for request in right:
            sequence.append(request)
            movement = movement + abs(current-request)
            current = request
        
        for request in reversed(left):
            sequence.append(request)
            movement = movement + abs(current-request)
            current = request
            
    return sequence,movement

head = 53
requests = [98, 183, 37, 122, 14, 124, 65, 67]
seq, mov = look(head, requests,"left")
print(seq)
print(mov) 

def clook(head,requests,direction):
    
    left = []
    right = []
    
    for request in requests:
        if request<head:
            left.append(request)
        else:
            right.append(request)
            
    left.sort()
    right.sort()
    
    sequence = []
    movement = 0
    current = head
    
    if direction == "left":
        for request in reversed(left):
            sequence.append(request)
            movement = movement + abs(current-request)
            current = request
            
        if right:    
            movement = movement + abs(current - right[-1])
            current = right[-1]
        
        for request in reversed(right):
            sequence.append(request)
            movement = movement + abs(current-request)
            current = request
            
    else :
        for request in right:
            sequence.append(request)
            movement = movement + abs(current-request)
            current = request
            
        if left:   
            movement = movement + abs(current - left[0])
            current = left[0]
        
        for request in left:
            sequence.append(request)
            movement = movement + abs(current-request)
            current = request
            
    return sequence,movement 

def make_plot(head, seq, algo_name):
    """
    Plot head movement path:
    x-axis: step number
    y-axis: head position
    """
    points = [head] + seq
    steps = list(range(len(points)))

    plt.figure()
    plt.plot(steps, points, marker="o")
    plt.title(f"Head Movement Path - {algo_name}")
    plt.xlabel("Step")
    plt.ylabel("Track / Cylinder")

    buffer = io.BytesIO()
    plt.savefig(buffer, format="png", bbox_inches="tight")
    plt.close()

    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return image_base64

# flask web
@app.route("/", methods=["GET", "POST"])
def index():
    results = None
    error = None
    best_algo = None
    best_movement = None

    if request.method == "POST":
        try:
            requests_list = []
            for x in request.form["requests"].split(","):
                x = x.strip()
                if x != "":
                    requests_list.append(int(x))

            head = int(request.form["head"])
            disk_size = int(request.form["disk_size"])
            direction = request.form["direction"]
            algo = request.form["algo"]

            results = {}

            if algo == "FCFS" or algo == "ALL":
                seq, mov = fcfs(head, requests_list)
                plot_file = make_plot(head, seq, "FCFS")
                results["FCFS"] = {"sequence": seq, "movement": mov, "plot": plot_file}

            if algo == "SSTF" or algo == "ALL":
                seq, mov = sstf(head, requests_list)
                plot_file = make_plot(head, seq, "SSTF")
                results["SSTF"] = {"sequence": seq, "movement": mov, "plot": plot_file}

            if algo == "SCAN" or algo == "ALL":
                seq, mov = scan(head, requests_list, disk_size, direction)
                plot_file = make_plot(head, seq, "SCAN")
                results["SCAN"] = {"sequence": seq, "movement": mov, "plot": plot_file}

            if algo == "C-SCAN" or algo == "ALL":
                seq, mov = cscan(head, requests_list, disk_size, direction)
                plot_file = make_plot(head, seq, "C-SCAN")
                results["C-SCAN"] = {"sequence": seq, "movement": mov, "plot": plot_file}

            if algo == "LOOK" or algo == "ALL":
                seq, mov = look(head, requests_list, direction)
                plot_file = make_plot(head, seq, "LOOK")
                results["LOOK"] = {"sequence": seq, "movement": mov, "plot": plot_file}

            if algo == "C-LOOK" or algo == "ALL":
                seq, mov = clook(head, requests_list, direction)
                plot_file = make_plot(head, seq, "C-LOOK")
                results["C-LOOK"] = {"sequence": seq, "movement": mov, "plot": plot_file}
                
            best_algo = None
            best_movement = None

            for name in results:
                movement = results[name]["movement"]

                if best_movement is None or movement < best_movement:
                    best_movement = movement
                    best_algo = name

        except Exception as e:
            error = str(e)

    return render_template(
        "index.html",
        results=results,
        error=error,
        best_algo=best_algo,
        best_movement=best_movement
    )

if __name__ == "__main__":
    app.run(debug=True)
