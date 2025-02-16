

class StickyNoteJson:
    
    def __init__(self, x:int, y:int, width:int, height:int, created_time:float, due_date = 0, content:str="", is_active=True, background_color="#FFEB3B"):
        self.relative_pos: list[int] = [x, y]
        self.width_height: list[int] = [width, height]
        self.created_time: int = created_time
        self.due_date: int = due_date
        self.content: str = content
        self.is_active: bool = is_active
        self.background_color = background_color
        
    
    def to_dict(self):
        return {
            "relative_pos": self.relative_pos,
            "width_height": self.width_height,
            "created_time": self.created_time,
            "due_date": self.due_date,
            "content": self.content,
            "is_active": self.is_active,
            "background_color": self.background_color
            }
    
    def __repr__(self):
        return "--Class: StickyNoteJson --\n"+str({
            "relative_pos": self.relative_pos,
            "width_height": self.width_height,
            "created_time": self.created_time,
            "due_date": self.due_date,
            "content": self.content,
            "is_active": self.is_active,
            "background_color": self.background_color
            })

    def to_str(self):
                return str({
            "relative_pos": self.relative_pos,
            "width_height": self.width_height,
            "created_time": self.created_time,
            "due_date": self.due_date,
            "content": self.content,
            "is_active": self.is_active,
            "background_color": self.background_color
            })