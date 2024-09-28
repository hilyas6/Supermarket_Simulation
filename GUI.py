"""
I have removed the  simulation running code at the end of main coursework code.
And replaced it with a new class called GUI which performs same tasks as last code.
however, in a gui form which can be run by using the buttons on the GUI.

Another change i made in the main code was adding in a new function called stop simulation which sets the stop event
thread to stop the simulation.
"""
import tkinter as tk
from BaseCode import *
import os

class GUI:
    def __init__(self, menu, regular_lane, self_service_lane):
        self.menu = menu
        menu.title("Supermarket Simulation")

        # Creating the instances
        self.lane_manager = LaneManager(regular_lane, self_service_lane)
        # settings the timings for the simulation
        self.total_simulation_duration = 270
        self.customer_generation_duration = 60
        self.display_status_interval = 15
        # setting a variable to keep track of simulation
        self.simulation_running = False

        # Set GUI background color using the colour code for light orange
        menu.configure(bg='#FFD700')

        # Creating a grid to position the buttons
        self.create_grid()
        # Creating the buttons for the gui  setting text on button and running the function made for them.
        self.run_button = tk.Button(menu, text="Run Simulation", command=self.start_simulation)
        self.run_button.configure(highlightbackground='#ADD8E6') # setting background colour for the button
        self.run_button.grid(row=1, column=3, pady=10) # positioning the button in the grid made

        self.stop_button = tk.Button(menu, text="Stop Simulation", command=self.stop_simulation, state=tk.DISABLED)
        self.stop_button.configure(highlightbackground='#ADD8E6')
        self.stop_button.grid(row=2, column=3, pady=5)

        self.customer_details_button = tk.Button(menu, text="Customer Details", command=self.customer_details)
        self.customer_details_button.configure(highlightbackground='#ADD8E6')
        self.customer_details_button.grid(row=3, column=3, pady=5)

        self.exit_button = tk.Button(menu, text="Exit", command=self.exit_simulation)
        self.exit_button.configure(highlightbackground='#ADD8E6')
        self.exit_button.grid(row=4, column=3, pady=5)

    # i have made a grid of 4x5 for the gui and given it its dimensions
    def create_grid(self):
        for i in range(1, 5):
            for j in range(1, 6):
                tk.Label(self.menu, text='', width=6, height=2, bg='#FFD700').grid(row=i, column=j)
    # This is the function to start the simulation it changes the state of the run and stop buttons when the simulation stops.
    def start_simulation(self):
        if not self.simulation_running:

            self.simulation_running = True
            self.run_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.customer_details_button.config(state=tk.NORMAL)
            self.exit_button.config(state=tk.NORMAL)

            self.simulation_thread = Thread(target=self.run_simulation)
            self.simulation_thread.start()
    # This function sets the simulation in place and changes the run and stop buttons states.
    def run_simulation(self):
        try:
            self.simulation = SupermarketSimulation(self.lane_manager)
            self.simulation.run_simulation(self.total_simulation_duration, self.customer_generation_duration,
                                           self.display_status_interval)
        except Exception as error:
            print(f"Simulation Error: {error}")
        finally:
            self.simulation_running = False
            self.run_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.customer_details_button.config(state=tk.NORMAL)
            self.exit_button.config(state=tk.NORMAL)      # Enable exit button after simulation
    # This function is set to the customer details button when pressed it displays the details of all the customers in
    # all of the lanes right now.
    def customer_details(self):
        total_customers_in_lanes = []

        for lane in self.lane_manager.regular_lane:
            total_customers_in_lanes.extend(lane.customers)

        total_customers_in_lanes.extend(self.lane_manager.self_service_lane.customers)

        if total_customers_in_lanes:
            for customer in total_customers_in_lanes:
                customer_details = f"\nCustomer {customer.identifier} details:\n" \
                                   f"Basket Size: {customer._Customer__basket_size}\n" \
                                   f"Checkout Time: {4 * customer._Customer__basket_size} seconds\n"\
                                   f"Lottery Ticket: {customer._Customer__lottery_ticket}\n"

                print(customer_details)
        else:
            print("No customers in the lanes.")
    # This function runs the function in the main code which stops the simulation.
    def stop_simulation(self):
        self.simulation.stop_simulation()
    # This function exits from the simulation exiting the program.
    def exit_simulation(self):
        os._exit(0)
        self.menu.destroy()


# This code runs the GUI class and ends the gui loop.
if __name__ == "__main__":
    gui_run = tk.Tk()
    gui_program = GUI(gui_run, regular_lane=[lane1, lane2, lane3, lane4, lane5], self_service_lane=ss1)
    gui_run.mainloop()

