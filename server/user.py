class User:
    def __init__(self, sid, name, team, role):
        self.sid = sid
        self.username = name
        self.team = team
        self.role = role

    def __str__(self):
        return f"{self.sid} {self.username} {self.team} {self.role}"

if __name__ == "__main__":
    u = User(1, "Test", "Test", "Test")
