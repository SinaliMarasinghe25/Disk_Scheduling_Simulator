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