import gtk, gobject


class AnimalBookingSystem:
       
    def get_contents(self):
        box = gtk.VPaned()
        box.add1(self.create_procedure_list())
        box.add2(self.create_animal_list())
        return box
 
    def create_booking_list(self):
        self.booking_model = gtk.ListStore(str, str)
        self.booking_list = gtk.TreeView(self.booking_model)
        self.booking_list.set_name("booked animals")
        cell_renderer = gtk.CellRendererText()
        self.booking_list.append_column(gtk.TreeViewColumn("booked animals", 
                                                       cell_renderer, text=0))
        cell_renderer_type = gtk.CellRendererText()
        self.booking_list.append_column(gtk.TreeViewColumn("", 
                                                       cell_renderer_type, text=1))
        
        return self.booking_list

    def create_animal_list(self):
        self.animal_model = gtk.ListStore(str, str, bool, bool)
        self.filtered_animal_model = self.animal_model.filter_new()
        self.filtered_animal_model.set_visible_column(2)
        self.animal_list = gtk.TreeView(self.filtered_animal_model)
        self.animal_list.set_name("available animals")
        cell_renderer_toggle = gtk.CellRendererToggle()
        self.animal_list.append_column(gtk.TreeViewColumn("is booked", 
                                                       cell_renderer_toggle, active=3))
        cell_renderer_toggle.connect("toggled", self.select_animal)
        cell_renderer_toggle.set_property('activatable', True)
       
        cell_renderer = gtk.CellRendererText()
        self.animal_list.append_column(gtk.TreeViewColumn("available animals", 
                                                       cell_renderer, text=0))
        cell_renderer_type = gtk.CellRendererText()
        self.animal_list.append_column(gtk.TreeViewColumn("animal type", 
                                                       cell_renderer_type, text=1))
        self.animal_list.get_selection().set_mode(gtk.SELECTION_NONE)
        
        self.animal_model.append(["Sunshine", "mare", True, False])
        self.animal_model.append(["Foggy", "goat", True, False])
        self.animal_model.append(["Cloudy", "goat", True, False])
        self.animal_model.append(["Lightning", "gelding", True, False])
        self.animal_model.append(["Misty", "mare", True, False])
        
        return self.animal_list
    
    def select_animal(self, cell, path):
        real_path = self.filtered_animal_model.convert_path_to_child_path(path)
        self.animal_model[real_path][3] = not self.animal_model[real_path][3]
    
    def create_procedure_list(self):
        
        self.procedure_model = gtk.ListStore(str, gobject.TYPE_PYOBJECT)
        self.procedure_list = gtk.TreeView(self.procedure_model)
        self.procedure_list.set_name("available procedures")
        cell_renderer = gtk.CellRendererText()
        self.procedure_list.append_column(gtk.TreeViewColumn("available procedures", 
                                                       cell_renderer, text=0))
        
        self.procedure_model.append(["grooming", ["mare", "goat", "gelding"]])
        self.procedure_model.append(["re-shoe", ["mare", "gelding"]])
        self.procedure_model.append(["milking", ["goat", "mare"]])
        
        self.procedure_list.get_selection().connect("changed", self.filter_animals_by_procedure)
        return self.procedure_list
    
    def filter_animals_by_procedure(self, selection):
        model, tree_iter = selection.get_selected()
        if tree_iter is None:
            return
        supported_animals = model.get_value(tree_iter, 1)
        
        for animal_data in self.animal_model:
            should_be_shown = animal_data[1] in supported_animals
            animal_data[2] = should_be_shown
            # bug! to remove, uncomment these lines
            if not should_be_shown:
                animal_data[3] = False
            
                

if __name__ == "__main__":
    window = gtk.Window()
    window.set_title("Book Animals for Procedures")
    window.connect("delete-event", gtk.main_quit)
    booking_system = AnimalBookingSystem()
    window.add(booking_system.get_contents())
    
    window.show_all()
    gtk.main()