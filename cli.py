import click
from database import Session  # Import session from the database module
from models import User

@click.command()
def main():
    """Main entry point to Reflectra"""
    click.echo("Welcome to Reflectra!")
    click.echo("Please choose an option:")
    click.echo("1. Register")
    click.echo("2. Login")
    
    choice = click.prompt("Enter your choice (1/2)", type=int)
    
    if choice == 1:
        register_user()
    elif choice == 2:
        login_user()
    else:
        click.echo("Invalid choice. Please restart and select 1 or 2.")

def register_user():
    """Handles user registration"""
    name = click.prompt("Your name")
    email = click.prompt("Your email")
    password = click.prompt("Password", hide_input=True)
    password_confirm = click.prompt("Repeat for confirmation", hide_input=True)
    
    if password == password_confirm:
        user = User(name=name, email=email, password=password)
        Session.add(user)
        Session.commit()
        click.echo(f"User {name} registered successfully!")
    else:
        click.echo("Passwords do not match! Please try again.")

def login_user():
    """Handles user login"""
    email = click.prompt("Your email")
    password = click.prompt("Password", hide_input=True)
    
    user = Session.query(User).filter_by(email=email, password=password).first()
    
    if user:
        click.echo(f"Login successful! Welcome, {user.name}.")
    else:
        click.echo("Invalid email or password. Please try again.")

if __name__ == "__main__":
    main()
