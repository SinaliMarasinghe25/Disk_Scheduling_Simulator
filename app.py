def fcfs (head,requests):
    sequence = []
    movement = 0
    current = head
    
    for request in requests:
        sequence.append(request)
        movement = movement + abs(current-request)
        current = request
        
    return sequence,movement

head = 53
requests = [98, 183, 37, 122, 14, 124, 65, 67]
seq, mov = fcfs(head, requests)
print(seq)
print(mov)

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