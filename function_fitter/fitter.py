from random import randint
import pygame
from math import cos

# highest acceptable err
ERROR_THRESHHOLD = 0.1
GRADIENT_OFFSET = 0.0001 # amount we offset gradient
DESCENT_STEP = 0.0001

GRAPH_RENDER_ACCURACY = 200

GRADIENT_MUL = 1/GRADIENT_OFFSET # for speed to avoid computign /GRDIENT_OFFSET each tme


# computes sqaure error of a function to a dataset
def squared_error(dataset, function, parameters):
    error = 0

    for data_x, data_y in dataset:
        y_predicted = function(data_x, parameters)
        delta_y = (y_predicted - data_y)
        error += delta_y * delta_y # summing up square errors at each point
    
    return error / len(parameters)**2


def error_gradient(dataset, function, parameters):
    gradient = [0 for _ in range(len(parameters))]

    # value with no offset
    basevalue = squared_error(dataset, function, parameters)

    # computing gradient for each parameter
    ssq = 0
    for i in range(len(gradient)):
        parameters[i] += GRADIENT_OFFSET

        # essentially doing f(x+h) - f(x) all over h over one axis (one parameter)
        gradient[i] = min((squared_error(dataset, function, parameters) - basevalue) * GRADIENT_MUL,100)

        # reset offset parameters for next computation
        parameters[i] -= GRADIENT_OFFSET
    
    return gradient



# IF it works, this function will return the parameters that minimize
# the error to our dataset
def solve(dataset, function, num_parameters, max_steps=10000, start_params=None, gradient_function=None):
    # we choose our initial parameters randomly
    
    if start_params is None:
        curr_params = [randint(-1,1) for _ in  range(num_parameters)]
    else:
        curr_params = start_params[:]


    # KEEP  improving our parameters until we reach an acceptable error
    error = squared_error(dataset, function, curr_params)
    gradient = None
    for _ in range(max_steps):
        if gradient_function is None:
            gradient = error_gradient(dataset, function, curr_params)
        else:
            # ignore for now
            gradient = None

        curr_params = [curr_param - grad_value * DESCENT_STEP for curr_param, grad_value in zip(curr_params, gradient)]


        error = squared_error(dataset, function, curr_params)
    return curr_params, error


def animated_solve(dataset, function, num_parameters):
    curr_params, error = solve(dataset, function, num_parameters, 1)

    ww, wh = 1000, 800
    wnd = pygame.display.set_mode((ww,wh))

    clock = pygame.time.Clock()
    fps = 120
    dt = 1/fps

    # fitting function to screen by finding min/max x/y lol
    sorted_x = list(sorted(dataset, key=lambda point: point[0]))
    sorted_y = list(sorted(dataset, key=lambda point: point[1]))
    xi, xf =  sorted_x[0][0], sorted_x[-1][0]
    yi, yf = sorted_y[0][1], sorted_y[-1][1]

    cx,cy = (xi+xf)/2, (yi+yf)/2
    xr, yr = 1.25*(xf-xi), 1.25*(yf-yi)

    def to_screen(p):
        y = -(p[-1] - cy) # (cx,cy) goes to 0, y gets flipped (cus pixels go down)
        x = p[0] - cx
        x /= xr  #  goes to (-0.5, 0.5) basically
        y /= yr
        x += 0.5 #  goes to [-1, 1]
        y += 0.5
        x *= ww # fits to screen
        y *= wh
        return (x,y)

    running = True
    while running:
        wnd.fill((0,0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 
        
        for point in dataset:
            pygame.draw.circle(wnd, (255,0,0), to_screen(point), 5)

        prev = None
        for i in range(GRAPH_RENDER_ACCURACY):
            currx = cx +  (i - GRAPH_RENDER_ACCURACY/2) * xr / GRAPH_RENDER_ACCURACY
            curr = (currx, function(currx, curr_params))
            if prev is not None:
                pygame.draw.line(wnd, (255,255,255), to_screen(curr), to_screen(prev),3)
            prev = curr
        
        curr_params, error = solve(dataset, function, len(curr_params), 100, curr_params)
        #print(f"Error is : {error} with params : {curr_params}")

        pygame.display.flip()
        clock.tick(fps)

    print(f"EXITED WITH ERROR: {error}")
    print("SUCCESSFULLY CONVERGED" if error < ERROR_THRESHHOLD else "FAILED TO CONVERGE")
    return curr_params

    
if __name__ == '__main__':

    def test_function(x, params):
        return params[0]*cos(0.1*x**2) + params[1]*cos(x*2 - 4) + params[2]*x**2+params[3]
    
    test_params = [-10,10,-0.2,-5]
    dataset = [(x,test_function(x, test_params)) for x in range(-10,10) ]

    print("--------------------------------")
    print("TESTING ANIMATED FUNCTION FILTER")
    print("--------------------------------")
    #print(f"TEST PARAMS ARE: {test_params} ON POINTS {dataset}")

    animated_solve(dataset, test_function, len(test_params))
    



