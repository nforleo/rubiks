import rubik
import copy

def shortest_path(start, end):
    """
    Using 2-way BFS, finds the shortest path from start_position to
    end_position. Returns a list of moves. 
    Assumes the rubik.quarter_twists move set.
    """
 
    """
    INVARIANTS:
        Loop Invariant: While there are elements in the Western frontier, we alternate
                        generating new states in each frontier and compare them until
                        either a match is found or the maximum amount of iterations
                        has been reached, which means there is no valid solution.
       
        Initialization: We check the starting state and ending state.  The frontiers
                        are empty because if the start and end state are the same,
                        we are done.

        Maintenance: The frontier contains all possible configurations that are derived
                    from the previous states and that we have not checked yet.  First, the
                    western frontier is generated and compared to the Eastern frontier.  If  
                    there is no match, the Eastern frontier is generated and compared to the
                    western front.  If a match is found, we are done.
                  
        Termination: There has either been 7 unsuccessful iterations, which means there is
                    an invalid cube configuration, and "None" is returned or a match has been 
                    found between the two frontiers and a list contating the valid moves is
                    returned.
    """
    # If the start is the same as the end, we are done
    if (start == end):
        return []
    
    # Frontier level start
    i = 0
 
    # Frontier of unvisited configurations for start and end
    western_front = {}
    eastern_front = {}
    
    # Initialize Frontiers
    # Frontiers are represented as dictionaries with keys representing configuration
    #   and the corresponding values representing the path to them.
    # Western frontier = from start point
    western_front[start] = []
    # Eastern frontier = from end point
    eastern_front[end] = []
    
    # While there are configs to be visited
    while(western_front):
        next = {}
        # Loop through each config in the start frontier
        for v in western_front:
            # Loop through and apply each move to each element of start frontier
            for perm in rubik.quarter_twists:
                temp = rubik.perm_apply(perm, v)
                if(temp not in western_front):
                    next[temp] = western_front[v] + [perm]
                    # If the config in starting frontier is in ending frontier, return
                    if(temp in eastern_front):
                        ret = []
                        for n in reversed(eastern_front[temp]):
                            ret = ret + [rubik.perm_inverse(n)]
                        return next[temp] + ret
        western_front = next
    
        next = {}
        
        # While there are configs to be visited in the ending frontier
        for v in eastern_front:
            # Loop through and apply each move to each element of the ending frontier
            for perm in rubik.quarter_twists:
                temp = rubik.perm_apply(perm, v)
                if(temp not in eastern_front):
                    next[temp] = eastern_front[v] + [perm]
                    # check other frontier
                    if(temp in western_front):
                        ret = []
                        for n in reversed(next[temp]):
                            ret = ret + [rubik.perm_inverse(n)]
                        return western_front[temp] + ret
                    
        eastern_front = next 
        # 2x2 Rubiks cubes have a maximum path length of 14, if we cannot find a solution in these
        # steps, the configuration was wrong to begin with.
        i += 1
        if (i > 7):
            return None
    return None