import click
from database import SessionLocal, init_db
from models import User, JournalEntry, MoodPattern
from datetime import date
import random
from collections import defaultdict

@click.group()
def cli():
    """Main entry point to Reflectra"""
    pass

@cli.command()
def init():
    """Initializes the database (run this before using Reflectra)"""
    init_db()
    click.echo("Database initialized!")

@cli.command()
def start():
    """Start the Reflectra application"""
    main()

def main():
    """Main menu for Reflectra"""
    while True:
        click.echo("\n--- Main Menu ---")
        click.echo("1. Register")
        click.echo("2. Login")
        click.echo("3. Exit")
        
        try:
            choice = click.prompt("Enter your choice (1-3)", type=int)
        except ValueError:
            click.echo("Invalid input. Please enter a number between 1 and 3.")
            continue
        
        if choice == 1:
            register()
        elif choice == 2:
            login()
        elif choice == 3:
            click.echo("Goodbye!")
            break
        else:
            click.echo("Invalid choice. Please enter a number between 1 and 3.")

def register():
    """Handles user registration"""
    while True:
        try:
            name = click.prompt("Your name")
            email = click.prompt("Your email")
            password = click.prompt("Password", hide_input=True)
            password_confirm = click.prompt("Repeat password", hide_input=True)
            
            if password == password_confirm:
                user = User(name=name, email=email, password=password)
                with SessionLocal() as session:
                    session.add(user)
                    session.commit()
                click.echo(f"User {name} registered successfully!")
                break
            else:
                click.echo("Passwords do not match. Please try again.")
        except Exception as e:
            click.echo(f"An error occurred: {e}. Please try again.")

def login():
    """Handles user login and provides access to journal entry management"""
    while True:
        try:
            email = click.prompt("Your email")
            password = click.prompt("Password", hide_input=True)
            
            with SessionLocal() as session:
                user = session.query(User).filter_by(email=email, password=password).first()
            
            if user:
                click.echo(f"Login successful! Welcome, {user.name}.")
                journal_entry_menu(user)
                break
            else:
                click.echo("Invalid email or password. Please try again.")
        except Exception as e:
            click.echo(f"An error occurred: {e}. Please try again.")

def journal_entry_menu(user):
    """Journal entry management menu for the logged-in user"""
    while True:
        try:
            click.echo("\n--- Journal Entry Menu ---")
            click.echo("1. Create Journal Entry")
            click.echo("2. View Journal Entries")
            click.echo("3. Analyze Mood Patterns")  
            click.echo("4. Update a Journal Entry")
            click.echo("5. Delete a Journal Entry")
            click.echo("6. Logout")
            
            choice = click.prompt("Enter your choice (1-6)", type=int)
        except ValueError:
            click.echo("Invalid input. Please enter a number between 1 and 6.")
            continue
        
        if choice == 1:
            create_journal_entry(user)
        elif choice == 2:
            view_journal_entries(user)
        elif choice == 3:
            analyze_mood_patterns(user)
        elif choice == 4:
            update_journal_entry(user)
        elif choice == 5:
            delete_journal_entry(user)
        elif choice == 6:
            click.echo("Logged out successfully!")
            break
        else:
            click.echo("Invalid choice. Please enter a number between 1 and 6.")

def create_journal_entry(user):
    """Creates a new journal entry for the logged-in user"""
    mood = click.prompt("How are you feeling today?")
    content = click.prompt("What's on your mind?", default="", show_default=False)
    entry = JournalEntry(user_id=user.id, date=date.today(), mood=mood, content=content)
    
    with SessionLocal() as session:
        session.add(entry)
        session.commit()
    click.echo("Journal entry created successfully!")
    
    # Update mood patterns based on the new entry
    update_mood_patterns(user, mood)

    # Display suggestions and motivational quote
    suggest_journal_entry(user)
    display_motivational_quote()

def view_journal_entries(user):
    """View all journal entries for the logged-in user"""
    with SessionLocal() as session:
        entries = session.query(JournalEntry).filter_by(user_id=user.id).all()
    
    if not entries:
        click.echo("No journal entries found.")
        return

    click.echo("\n--- Your Journal Entries ---")
    for entry in entries:
        click.echo(f"[{entry.date}] Mood: {entry.mood}\n{entry.content}\n")

def update_journal_entry(user):
    """Update an existing journal entry"""
    with SessionLocal() as session:
        entries = session.query(JournalEntry).filter_by(user_id=user.id).all()
    
    if not entries:
        click.echo("No journal entries found to update.")
        return

    click.echo("\n--- Select Entry to Update ---")
    for index, entry in enumerate(entries):
        click.echo(f"{index + 1}. [{entry.date}] Mood: {entry.mood}\n{entry.content}")

    try:
        choice = click.prompt("Enter the number of the entry to update", type=int) - 1
        if choice < 0 or choice >= len(entries):
            click.echo("Invalid choice.")
            return

        mood = click.prompt("New mood", default=entries[choice].mood)
        content = click.prompt("New content", default=entries[choice].content)
        entries[choice].mood = mood
        entries[choice].content = content

        session.commit()
        click.echo("Journal entry updated successfully!")
    except Exception as e:
        click.echo(f"An error occurred while updating the entry: {e}")

def delete_journal_entry(user):
    """Delete a specific journal entry"""
    with SessionLocal() as session:
        entries = session.query(JournalEntry).filter_by(user_id=user.id).all()
    
    if not entries:
        click.echo("No journal entries found to delete.")
        return

    click.echo("\n--- Select Entry to Delete ---")
    for index, entry in enumerate(entries):
        click.echo(f"{index + 1}. [{entry.date}] Mood: {entry.mood}\n{entry.content}")

    try:
        choice = click.prompt("Enter the number of the entry to delete", type=int) - 1
        if choice < 0 or choice >= len(entries):
            click.echo("Invalid choice.")
            return

        session.delete(entries[choice])
        session.commit()
        click.echo("Journal entry deleted successfully!")
    except Exception as e:
        click.echo(f"An error occurred while deleting the entry: {e}")

def update_mood_patterns(user, mood):
    """Updates mood patterns based on the latest journal entry."""
    with SessionLocal() as session:
        mood_pattern = session.query(MoodPattern).filter_by(user_id=user.id).first()
        
        if mood_pattern:
            mood_pattern.pattern += f", {mood}"  
            session.commit()
        else:
            new_pattern = MoodPattern(user_id=user.id, pattern=mood)
            session.add(new_pattern)
            session.commit()
        
        click.echo(f"Mood pattern updated: {mood}")

def suggest_journal_entry(user):
    """Suggest journal entry topics based on past mood patterns."""
    with SessionLocal() as session:
        entries = session.query(JournalEntry).filter_by(user_id=user.id).order_by(JournalEntry.date.desc()).limit(5).all()
    
    if not entries:
        click.echo("No recent journal entries available for suggestions.")
        return

    recent_moods = [entry.mood for entry in entries]
    mood_counts = {mood: recent_moods.count(mood) for mood in set(recent_moods)}
    most_common_mood = max(mood_counts, key=mood_counts.get)

    suggestions = {
        'happy': "You seem to be in good spirits lately! Write about what’s been bringing you joy.",
        'sad': "It's okay to feel down. Maybe journaling about your thoughts can help.",
        'neutral': "Reflect on your day-to-day. What small changes could bring more joy?",
        'stressed': "It seems like stress has been present. How do you cope with it?",
    }

    suggestion = suggestions.get(most_common_mood, "How about reflecting on your recent experiences?")
    click.echo(f"\n--- Journal Entry Suggestion ---\n{suggestion}")

def display_motivational_quote():
    """Display a random motivational quote after a journal entry."""
    motivational_quotes = [
        "Believe in yourself! You are capable of more than you know.",
        "This too shall pass.",
        "Every day is a new beginning. Take a deep breath and start again.",
        "You are stronger than you think.",
        "Positivity always wins!"
    ]
    quote = random.choice(motivational_quotes)
    click.echo(f"\n--- Daily Affirmation ---\n{quote}")

def analyze_mood_patterns(user):
    """Analyzes mood patterns for the user"""
    with SessionLocal() as session:
        patterns = session.query(MoodPattern).filter_by(user_id=user.id).first()

    if not patterns:
        click.echo("No mood patterns found for analysis.")
        return

    pattern_list = patterns.pattern.split(", ")
    mood_frequency = defaultdict(int)

    for mood in pattern_list:
        mood_frequency[mood] += 1

    # Display mood statistics
    click.echo("\n--- Mood Statistics ---")
    for mood, count in mood_frequency.items():
        click.echo(f"{mood}: {count} times")

    # Calculate and display average mood
    mood_scale = {
        "very_happy": 5,
        "happy": 4,
        "neutral": 3,
        "sad": 2,
        "very_sad": 1,
    }
    
    total_mood_value = sum(mood_scale.get(mood, 3) * count for mood, count in mood_frequency.items())
    total_entries = sum(mood_frequency.values())
    average_mood = total_mood_value / total_entries if total_entries > 0 else 3  # Default to neutral
    click.echo(f"Average mood: {average_mood:.2f} (on a scale of 1-5)")

    # Prompt for feedback
    feedback = click.prompt("Do you feel this analysis reflects your mood trends? (yes/no)", type=str)
    click.echo(f"Feedback received: {feedback}")

    # Respond to feedback
    if feedback.lower() == 'no':
        click.echo("I'm sorry to hear that! Can you tell me what you feel was missing in this analysis?")
        specific_feedback = click.prompt("Your thoughts: ")

    # Provide suggestions based on mood
    if average_mood < 3:
        click.echo("It seems like your average mood is leaning towards the negative side. Here are some suggestions:")
        click.echo("- Consider taking a short walk to clear your mind.")
        click.echo("- Try writing down things you're grateful for.")
        click.echo("- Remember to reach out to friends or loved ones for support.")
    elif average_mood > 4:
        click.echo("Great to see your mood is positive! Keep it up!")
    else:
        click.echo("Your mood seems neutral. Perhaps engage in an activity that brings you joy!")

if __name__ == "__main__":
    cli()
