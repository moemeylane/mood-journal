import click
from database import SessionLocal, init_db
from models import User, JournalEntry
from datetime import date

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
    # No need to call main directly here. Click will handle command execution.
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

@cli.command()
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

@cli.command()
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
            click.echo("3. Update a Journal Entry")
            click.echo("4. Delete a Journal Entry")
            click.echo("5. Logout")
            
            try:
                choice = click.prompt("Enter your choice (1-5)", type=int)
            except ValueError:
                click.echo("Invalid input. Please enter a number between 1 and 5.")
                continue
            
            if choice == 1:
                create_journal_entry(user)
            elif choice == 2:
                view_journal_entries(user)
            elif choice == 3:
                update_journal_entry(user)
            elif choice == 4:
                delete_journal_entry(user)
            elif choice == 5:
                click.echo("Logged out successfully.")
                break
            else:
                click.echo("Invalid choice. Please enter a number between 1 and 5.")
        except Exception as e:
            click.echo(f"An error occurred: {e}. Please try again.")

def create_journal_entry(user):
    """Creates a new journal entry for the logged-in user"""
    mood = click.prompt("How are you feeling today?")
    content = click.prompt("What's on your mind?", default="", show_default=False)
    entry = JournalEntry(user_id=user.id, date=date.today(), mood=mood, content=content)
    with SessionLocal() as session:
        session.add(entry)
        session.commit()
    click.echo("Journal entry created successfully!")

def view_journal_entries(user):
    """Displays all journal entries for the logged-in user"""
    with SessionLocal() as session:
        entries = session.query(JournalEntry).filter_by(user_id=user.id).all()
    if entries:
        for entry in entries:
            click.echo(f"{entry.id}: {entry.date}: {entry.mood} - {entry.content}")
    else:
        click.echo("No journal entries found.")

def update_journal_entry(user):
    """Updates an existing journal entry"""
    while True:
        try:
            entry_id = click.prompt("Enter the ID of the entry to update", type=int)
            with SessionLocal() as session:
                entry = session.query(JournalEntry).filter_by(id=entry_id, user_id=user.id).first()

            if entry:
                mood = click.prompt(f"Update mood (current: {entry.mood})", default=entry.mood)
                content = click.prompt(f"Update content (current: {entry.content})", default=entry.content)
                
                # Update the entry
                entry.mood = mood
                entry.content = content
                session.commit()
                
                click.echo("Journal entry updated successfully!")
                break
            else:
                click.echo("Journal entry not found or you do not have permission to edit it. Please try again.")
        except Exception as e:
            click.echo(f"An error occurred: {e}. Please try again.")

def delete_journal_entry(user):
    """Deletes a journal entry"""
    entry_id = click.prompt("Enter the ID of the entry to delete", type=int)
    with SessionLocal() as session:
        entry = session.query(JournalEntry).filter_by(id=entry_id, user_id=user.id).first()

    if entry:
        session.delete(entry)
        session.commit()
        click.echo("Journal entry deleted successfully!")
    else:
        click.echo("Journal entry not found.")

if __name__ == "__main__":
    cli()
