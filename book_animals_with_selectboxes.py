import gtk, gobject


class AnimalBookingSystem:
       
    def get_contents(self):
        box = gtk.HPaned()
        box.add1(self.create_procedure_list())
        animal_box = gtk.VBox()
        animal_box.pack_start(self.create_animal_list())
        animal_box.pack_start(self.create_book_button())
        box.add2(animal_box)
        vbox = gtk.VPaned()
        vbox.pack1(box)
        vbox.pack2(self.create_booking_list())
        return vbox
 
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
        self.animal_model = gtk.ListStore(str, str, bool)
        self.filtered_animal_model = self.animal_model.filter_new()
        self.filtered_animal_model.set_visible_column(2)
        self.animal_list = gtk.TreeView(self.filtered_animal_model)
        self.animal_list.set_name("available animals")
        cell_renderer = gtk.CellRendererText()
        cell_renderer_type = gtk.CellRendererText()
        self.animal_list.append_column(gtk.TreeViewColumn("available animals", 
                                                       cell_renderer, text=0))
        self.animal_list.append_column(gtk.TreeViewColumn("animal type", 
                                                       cell_renderer_type, text=1))
        self.animal_list.get_selection().set_mode(gtk.SELECTION_MULTIPLE)
        
        self.animal_model.append(["Sunshine", "mare", True])
        self.animal_model.append(["Foggy", "goat", True])
        self.animal_model.append(["Cloudy", "goat", True])
        self.animal_model.append(["Lightning", "gelding", True])
        self.animal_model.append(["Misty", "mare", True])
        
        return self.animal_list
    
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
            
        to_remove = []
        for animal_data in self.booking_model:
            is_suitable = animal_data[1] in supported_animals
            if not is_suitable:
                to_remove.append(animal_data)
                
        #for animal in to_remove:
        #    self.booking_model.remove(animal.iter)
            
    def create_book_button(self):
        button = gtk.Button("book")
        button.connect("clicked", self.make_booking)
        return button
    
    def make_booking(self, button):
        model, tree_paths = self.animal_list.get_selection().get_selected_rows()
        selected_animals = []
        for path in tree_paths:
            animal = model.get_iter(path)
            selected_animals.append([model.get_value(animal, 0), model.get_value(animal, 1)])
            
        model, tree_iter = self.procedure_list.get_selection().get_selected()
        if tree_iter is None:
            selected_procedure = "<none>"
        else:
            selected_procedure = model.get_value(tree_iter, 0)
        booking = "booked animal(s) %s" % (selected_animals)
        
        for animal in selected_animals:
            self.booking_model.append(animal)

if __name__ == "__main__":
    window = gtk.Window()
    window.set_title("Book Animals for Procedures")
    window.connect("delete-event", gtk.main_quit)
    booking_system = AnimalBookingSystem()
    window.add(booking_system.get_contents())
    
    window.show_all()
    gtk.main()
