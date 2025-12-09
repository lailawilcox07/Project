import random
import gradio as gr

# Global variables
game_array = []
game_target = 0
game_low = 0
game_high = 0
step_history = []

def generate_list():
    """Generate a sorted list and pick a target"""
    global game_array, game_target, game_low, game_high, step_history
    
    # Random array length between 6 and 16
    array_length = random.randint(6, 16)
    game_array = sorted(random.sample(range(1, 101), array_length))
    game_low = 0
    game_high = len(game_array) - 1
    step_history = []
    
    if random.random() < 0.7:
        game_target = random.choice(game_array)
    else:
        all_nums = set(range(1, 101))
        not_in_list = list(all_nums - set(game_array))
        game_target = random.choice(not_in_list)
    
    output = f"""
### Array: {', '.join(map(str, game_array))}

### Target Number: **{game_target}**

---
**Click 'Start Your Binary Search' to begin**
"""
    
    return (
        output, 
        gr.update(visible=False),  # hide generate button
        gr.update(visible=True),   # show start button
        gr.update(visible=False),  # middle_index
        gr.update(visible=False),  # middle_value
        gr.update(visible=False),  # submit
        gr.update(visible=False),  # left
        gr.update(visible=False),  # right
        gr.update(visible=False),  # found
        gr.update(visible=False),  # new game button
        ""  # history
    )

def start_search():
    """Start the search"""
    global game_array, game_target, game_low, game_high, step_history
    
    step_history = []
    
    # Top: Plain full array
    array_str = ", ".join(map(str, game_array))
    
    # Bottom: Full array with indices, bold only search section
    index_parts = []
    for i, val in enumerate(game_array):
        if game_low <= i <= game_high:
            index_parts.append(f"[{i}]: **{val}**")
        else:
            index_parts.append(f"[{i}]: {val}")
    index_display = " | ".join(index_parts)
    
    output = f"""
### Array: {array_str}

### Target: **{game_target}**

---

### Indices and Current Search Range Bolded:
{index_display}

---
**Step 1:** Find the middle value

Enter the middle **index** and its **value**
"""
    
    return (
        output,
        gr.update(visible=False),  # start button disappears
        gr.update(visible=True, value=None),   # middle_index
        gr.update(visible=True, value=None),   # middle_value
        gr.update(visible=True),   # submit
        gr.update(visible=False),  # left
        gr.update(visible=False),  # right
        gr.update(visible=False),  # found
        gr.update(visible=False),  # new_game_btn (keep hidden during play)
        ""  # history
    )

def check_middle(middle_idx, middle_val):
    """Check if the user got the middle correct"""
    global game_array, game_target, game_low, game_high, step_history
    
    # Use the standard binary search formula: (high - low) // 2
    mid_index_in_subarray = (game_high - game_low) // 2
    actual_mid_index = game_low + mid_index_in_subarray
    mid_value = game_array[actual_mid_index]
    
    try:
        user_idx = int(middle_idx)
        user_val = int(middle_val)
    except:
        # Show error but keep the display intact
        error_msg = f"<div style='background-color: #f8d7da; padding: 10px; border-radius: 5px; color: #000000; margin-bottom: 10px;'><span style='color: #8b0000; font-weight: bold;'>ERROR:</span> Please enter valid numbers (integers only)</div>"
        error_history = "".join(step_history) + error_msg
        
        # Top: Plain full array
        array_str = ", ".join(map(str, game_array))
        
        # Bottom: Full array with indices, bold only search section
        index_parts = []
        for i, val in enumerate(game_array):
            if game_low <= i <= game_high:
                index_parts.append(f"[{i}]: **{val}**")
            else:
                index_parts.append(f"[{i}]: {val}")
        index_display = " | ".join(index_parts)
        
        output = f"""
### Array: {array_str}

### Target: **{game_target}**

---

### Indices and Current Search Range Bolded:
{index_display}

---
**Please try again:** Find the middle value

Enter the middle **index** and its **value**
"""
        
        return (
            output,
            gr.update(),  # start
            gr.update(visible=True),  # middle_index - keep visible
            gr.update(visible=True),  # middle_value - keep visible
            gr.update(visible=True),  # submit - keep visible
            gr.update(visible=False),  # left
            gr.update(visible=False),  # right
            gr.update(visible=False),  # found
            gr.update(visible=False),  # new_game_btn
            error_history
        )
    
    # Compare with the actual index in the FULL array
    if user_idx == actual_mid_index and user_val == mid_value:
        feedback = f"<span style='color: #004d00; font-weight: bold;'>CORRECT</span> Middle index: {actual_mid_index}, Middle value: {mid_value}"
        color = "#d4edda"  # Light green background
    else:
        feedback = f"<span style='color: #8b0000; font-weight: bold;'>INCORRECT</span> Middle index is: {actual_mid_index}, Middle value is: {mid_value}"
        color = "#f8d7da"  # Light pink background
    
    history_entry = f"<div style='background-color: {color}; padding: 10px; border-radius: 5px; color: #000000; margin-bottom: 10px;'>{feedback}</div>"
    step_history.append(history_entry)
    
    # Top: Plain full array
    array_str = ", ".join(map(str, game_array))
    
    # Bottom: Full array with indices, bold search section, mark middle
    # (actual_mid_index already calculated above)
    index_parts = []
    for i, val in enumerate(game_array):
        if i == actual_mid_index:
            index_parts.append(f"[{i}]: **{val}** MIDDLE")
        elif game_low <= i <= game_high:
            index_parts.append(f"[{i}]: **{val}**")
        else:
            index_parts.append(f"[{i}]: {val}")
    
    index_display = " | ".join(index_parts)
    
    # Check if found
    if mid_value == game_target:
        final_feedback = f"<div style='background-color: #d4edda; padding: 20px; border-radius: 5px; color: #000000; text-align: center; font-size: 18px;'><span style='color: #004d00; font-weight: bold;'>CONGRATULATIONS!</span><br>You found <span style='color: #004d00; font-weight: bold;'>{game_target}</span> in the array!</div>"
        step_history.append(final_feedback)
        
        output = f"""
### Array: {array_str}

### Target: **{game_target}** (TARGET FOUND)

---

**Game Over!** Click the button below to play again
"""
        
        history_display = "".join(step_history)
        return (
            output,
            gr.update(),  # start (already hidden)
            gr.update(visible=False),  # middle_index
            gr.update(visible=False),  # middle_value
            gr.update(visible=False),  # submit
            gr.update(visible=False),  # left
            gr.update(visible=False),  # right
            gr.update(visible=False),  # found button (keep hidden)
            gr.update(visible=True),   # new game button (show this)
            history_display
        )
    
    # Ask for direction
    output = f"""
### Array: {array_str}

### Target: **{game_target}**

---

### Indices and Current Search Range Bolded:
{index_display}

---
**Which half should we search?**

Target **{game_target}** vs Middle **{mid_value}**

Choose a direction:
"""
    
    history_display = "".join(step_history)
    return (
        output,
        gr.update(),  # start
        gr.update(visible=False),  # middle_index
        gr.update(visible=False),  # middle_value
        gr.update(visible=False),  # submit
        gr.update(visible=True),   # left
        gr.update(visible=True),   # right
        gr.update(visible=False),  # found
        gr.update(visible=False),  # new_game_btn (keep hidden)
        history_display
    )

def choose_left():
    """User chose left"""
    global game_array, game_target, game_low, game_high, step_history
    
    # Use the correct binary search formula
    mid_index_offset = (game_high - game_low) // 2
    actual_mid_index = game_low + mid_index_offset
    mid_value = game_array[actual_mid_index]
    
    correct = game_target < mid_value
    
    if correct:
        feedback = f"<span style='color: #004d00; font-weight: bold;'>CORRECT</span> Target ({game_target}) < Middle ({mid_value}), so we search LEFT"
        color = "#d4edda"  # Light green background
    else:
        feedback = f"<span style='color: #8b0000; font-weight: bold;'>INCORRECT</span> Target ({game_target}) > Middle ({mid_value}), so we should search RIGHT"
        color = "#f8d7da"  # Light pink background
    
    history_entry = f"<div style='background-color: {color}; padding: 10px; border-radius: 5px; color: #000000; margin-bottom: 10px;'>{feedback}</div>"
    step_history.append(history_entry)
    
    # Update the search range based on what SHOULD happen
    if game_target < mid_value:
        game_high = actual_mid_index - 1
    else:
        game_low = actual_mid_index + 1
    
    return continue_search()

def choose_right():
    """User chose right"""
    global game_array, game_target, game_low, game_high, step_history
    
    # Use the correct binary search formula
    mid_index_offset = (game_high - game_low) // 2
    actual_mid_index = game_low + mid_index_offset
    mid_value = game_array[actual_mid_index]
    
    correct = game_target > mid_value
    
    if correct:
        feedback = f"<span style='color: #004d00; font-weight: bold;'>CORRECT</span> Target ({game_target}) > Middle ({mid_value}), so we search RIGHT"
        color = "#d4edda"  # Light green background
    else:
        feedback = f"<span style='color: #8b0000; font-weight: bold;'>INCORRECT</span> Target ({game_target}) < Middle ({mid_value}), so we should search LEFT"
        color = "#f8d7da"  # Light pink background
    
    history_entry = f"<div style='background-color: {color}; padding: 10px; border-radius: 5px; color: #000000; margin-bottom: 10px;'>{feedback}</div>"
    step_history.append(history_entry)
    
    # Update the search range based on what SHOULD happen
    if game_target > mid_value:
        game_low = actual_mid_index + 1
    else:
        game_high = actual_mid_index - 1
    
    return continue_search()

def target_found():
    """User confirmed target is found"""
    global game_array, game_target, step_history
    
    final_feedback = f"<div style='background-color: #d4edda; padding: 20px; border-radius: 5px; color: #000000; text-align: center; font-size: 18px;'><span style='color: #004d00; font-weight: bold;'>CONGRATULATIONS!</span><br>You found <span style='color: #004d00; font-weight: bold;'>{game_target}</span> in the array!</div>"
    step_history.append(final_feedback)
    
    output = f"""
### Array: {', '.join(map(str, game_array))}

### Target: **{game_target}** (TARGET FOUND)

---

**Game Over!** Click the button below to play again.
"""
    
    history_display = "".join(step_history)
    return (
        output,
        gr.update(),  # start
        gr.update(visible=False),  # middle_index
        gr.update(visible=False),  # middle_value
        gr.update(visible=False),  # submit
        gr.update(visible=False),  # left
        gr.update(visible=False),  # right
        gr.update(visible=False),  # found
        gr.update(visible=True),   # new game button
        history_display
    )

def continue_search():
    """Continue to next step"""
    global game_array, game_target, game_low, game_high, step_history
    
    # Check if exhausted
    if game_low > game_high:
        final_feedback = f"<div style='background-color: #fff3cd; padding: 20px; border-radius: 5px; color: #000000; text-align: center;'><span style='font-weight: bold;'>Search Complete!</span><br>The number <span style='font-weight: bold;'>{game_target}</span> is <span style='font-weight: bold;'>NOT in the list</span>.</div>"
        step_history.append(final_feedback)
        
        output = f"""
### Array: {', '.join(map(str, game_array))}

### Target: **{game_target}** (TARGET NOT FOUND)

---

**GAME OVER** Click the button below to play again
"""
        history_display = "".join(step_history)
        return (
            output,
            gr.update(),  # start
            gr.update(visible=False),  # middle_index
            gr.update(visible=False),  # middle_value
            gr.update(visible=False),  # submit
            gr.update(visible=False),  # left
            gr.update(visible=False),  # right
            gr.update(visible=False),  # found
            gr.update(visible=True),   # new game button
            history_display
        )
    
    # Top: Plain full array
    array_str = ", ".join(map(str, game_array))
    
    # Bottom: Full array with indices, bold only search section
    index_parts = []
    for i, val in enumerate(game_array):
        if game_low <= i <= game_high:
            index_parts.append(f"[{i}]: **{val}**")
        else:
            index_parts.append(f"[{i}]: {val}")
    
    index_display = " | ".join(index_parts)
    step_num = len(step_history) + 1
    
    output = f"""
### Array: {array_str}

### Target: **{game_target}**

---

### Indices and Current Search Range Bolded:
{index_display}

---
**Step {step_num}:** Find the middle value!

Enter the middle **index** and its **value**
"""
    
    history_display = "".join(step_history)
    return (
        output,
        gr.update(),  # start
        gr.update(visible=True, value=None),   # middle_index
        gr.update(visible=True, value=None),   # middle_value
        gr.update(visible=True),   # submit
        gr.update(visible=False),  # left
        gr.update(visible=False),  # right
        gr.update(visible=False),  # found
        gr.update(visible=False),  # new_game_btn
        history_display
    )

# Create interface
with gr.Blocks(title="Binary Search Game", theme=gr.themes.Soft()) as demo:
    gr.Markdown(
        """
        # Interactive Binary Search Game
        """
    )
    
    with gr.Row():
        generate_btn = gr.Button("Generate List & Target", variant="secondary", size="lg")
        start_btn = gr.Button("Start Your Binary Search", variant="primary", size="lg", visible=False)
    
    output_box = gr.Markdown("Click 'Generate List & Target' to begin!")
    
    with gr.Row():
        middle_index = gr.Number(label="Middle Index", precision=0, visible=False)
        middle_value = gr.Number(label="Middle Value", precision=0, visible=False)
    
    submit_btn = gr.Button("Submit Answer", variant="primary", visible=False)
    
    with gr.Row():
        left_btn = gr.Button("Search Left Half", variant="secondary", size="lg", visible=False)
        right_btn = gr.Button("Search Right Half", variant="secondary", size="lg", visible=False)
    
    found_btn = gr.Button("Target Found", variant="primary", size="lg", visible=False)
    
    gr.Markdown("### Step History")
    history_box = gr.HTML("")
    
    # Help/Info section
    with gr.Accordion("Help & Instructions", open=False):
        gr.Markdown(
            """
            ### How to Play Binary Search
            
            #### **Finding the Middle Index**
            
            To find the middle index of your current search range:
            
            1. **Identify your current range**: Look at the bolded numbers
            2. **Use this formula**: `Middle Index = Low Index + (High Index - Low Index) // 2`
            
            **Example:**
            - If searching indices **[2] to [9]**
            - Low = 2, High = 9
            - Middle = 2 + (9 - 2) // 2 = 2 + 3 = **5**
            
            ---
            
            #### **Choosing Left or Right**
            
            After finding the middle value, compare it with your target:
            
            - **Target < Middle Value** → Search **LEFT** (lower half)
            - **Target > Middle Value** → Search **RIGHT** (upper half)
            - **Target = Middle Value** → **Found it!** 
            
            **Example:**
            - Target: **45**, Middle Value: **60**
            - Since 45 < 60, search the **LEFT** half
            
            ---
            
            ### Goal
            Keep narrowing down your search range until you find the target (or determine it's not in the list)
            """
        )
    
    # New game button at the bottom
    new_game_btn = gr.Button("Generate New List", variant="primary", size="lg", visible=False)
    
    # Connect buttons
    generate_btn.click(
        fn=generate_list,
        inputs=[],
        outputs=[output_box, generate_btn, start_btn, middle_index, middle_value, submit_btn, left_btn, right_btn, found_btn, new_game_btn, history_box]
    )
    
    start_btn.click(
        fn=start_search,
        inputs=[],
        outputs=[output_box, start_btn, middle_index, middle_value, submit_btn, left_btn, right_btn, found_btn, new_game_btn, history_box]
    )
    
    submit_btn.click(
        fn=check_middle,
        inputs=[middle_index, middle_value],
        outputs=[output_box, start_btn, middle_index, middle_value, submit_btn, left_btn, right_btn, found_btn, new_game_btn, history_box]
    )
    
    left_btn.click(
        fn=choose_left,
        inputs=[],
        outputs=[output_box, start_btn, middle_index, middle_value, submit_btn, left_btn, right_btn, found_btn, new_game_btn, history_box]
    )
    
    right_btn.click(
        fn=choose_right,
        inputs=[],
        outputs=[output_box, start_btn, middle_index, middle_value, submit_btn, left_btn, right_btn, found_btn, new_game_btn, history_box]
    )
    
    found_btn.click(
        fn=target_found,
        inputs=[],
        outputs=[output_box, start_btn, middle_index, middle_value, submit_btn, left_btn, right_btn, found_btn, new_game_btn, history_box]
    )
    
    # New game button does the same as generate
    new_game_btn.click(
        fn=generate_list,
        inputs=[],
        outputs=[output_box, generate_btn, start_btn, middle_index, middle_value, submit_btn, left_btn, right_btn, found_btn, new_game_btn, history_box]
    )

if __name__ == "__main__":
    demo.launch(debug=True)