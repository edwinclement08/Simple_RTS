                elif event.buttons == (0, 0, 0) and (self.selected_unit or self.multiple_selected):
                    if self.parent.map.is_cell_free(x, y) and self.parent.game_data.is_place_empty(x, y):
                        if self.selected_unit and issubclass(self.selected_unit.__class__, unit_base.unit_attacking):
                            self.current_cursor = self.cursor_images["move"]
                        elif self.multiple_selected:
                            for q in self.multiple_selected:
                                if issubclass(q.__class__, unit_base.unit_attacking):
                                    self.current_cursor = self.cursor_images["move"]

                    elif not self.parent.game_data.is_place_empty(x, y):
                        if self.parent.game_data.get_unit(x, y)[0].allegiance == self.parent.computer:
                            one_attacking_unit = self.selected_unit\
                                and isinstance(self.selected_unit, self.parent.unit_base.unit_attacking)
                            self.multi_attacking_units = False
                            if not self.multiple_selected:
                                self.multi_attacking_units = False
                            else:
                                for k in self.multiple_selected:
                                    if isinstance(k, self.parent.unit_base.unit_attacking):
                                        self.multi_attacking_units = True
                                        break
                                else:
                                    self.multi_attacking_units = False
                            if one_attacking_unit or self.multi_attacking_units:
                                self.current_cursor = self.cursor_images["attack"]

                        elif self.parent.game_data.get_unit(x, y)[0].allegiance == self.parent.human:
                            self.current_cursor = self.cursor_images["select"]
                    else:
                        self.current_cursor = self.cursor_images["normal"]
