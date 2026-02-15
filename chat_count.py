course="Python Programming"
# Count character frequency in the course string
character_count = {}
for char in course:
    if char in character_count:
        character_count[char] += 1
    else:
        character_count[char] = 1

print("Character count in course:", character_count)