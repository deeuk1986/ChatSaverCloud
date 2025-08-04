import os
import logging
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from chat_storage import ChatStorage
import uuid
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "fallback_secret_key_for_dev")

# Initialize chat storage
chat_storage = ChatStorage()

@app.route('/')
def index():
    """Main dashboard displaying saved chats"""
    try:
        saved_chats = chat_storage.get_all_chats()
        return render_template('index.html', saved_chats=saved_chats)
    except Exception as e:
        logging.error(f"Error loading dashboard: {e}")
        flash('Error loading saved chats', 'error')
        return render_template('index.html', saved_chats=[])

@app.route('/save_chat', methods=['POST'])
def save_chat():
    """Save a new chat conversation"""
    try:
        chat_content = request.form.get('chat_content', '').strip()
        chat_title = request.form.get('chat_title', '').strip()
        
        if not chat_content:
            flash('Chat content cannot be empty', 'error')
            return redirect(url_for('index'))
        
        if not chat_title:
            chat_title = f"Chat {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        
        # Generate unique ID for the chat
        chat_id = str(uuid.uuid4())
        
        # Save chat to storage
        success = chat_storage.save_chat(chat_id, chat_title, chat_content)
        
        if success:
            flash(f'Chat "{chat_title}" saved successfully!', 'success')
        else:
            flash('Error saving chat', 'error')
            
    except Exception as e:
        logging.error(f"Error saving chat: {e}")
        flash('Error saving chat', 'error')
    
    return redirect(url_for('index'))

@app.route('/view/<chat_id>')
def view_chat(chat_id):
    """View a saved chat conversation (read-only)"""
    try:
        chat_data = chat_storage.get_chat(chat_id)
        
        if not chat_data:
            flash('Chat not found', 'error')
            return redirect(url_for('index'))
        
        return render_template('view_chat.html', chat_data=chat_data, chat_id=chat_id)
        
    except Exception as e:
        logging.error(f"Error viewing chat {chat_id}: {e}")
        flash('Error loading chat', 'error')
        return redirect(url_for('index'))

@app.route('/delete/<chat_id>', methods=['POST'])
def delete_chat(chat_id):
    """Delete a saved chat"""
    try:
        success = chat_storage.delete_chat(chat_id)
        
        if success:
            flash('Chat deleted successfully', 'success')
        else:
            flash('Error deleting chat', 'error')
            
    except Exception as e:
        logging.error(f"Error deleting chat {chat_id}: {e}")
        flash('Error deleting chat', 'error')
    
    return redirect(url_for('index'))

@app.route('/get_share_link/<chat_id>')
def get_share_link(chat_id):
    """Generate shareable link for a chat"""
    try:
        # Verify chat exists
        chat_data = chat_storage.get_chat(chat_id)
        if not chat_data:
            return jsonify({'error': 'Chat not found'}), 404
        
        # Generate full URL for sharing
        share_url = url_for('view_chat', chat_id=chat_id, _external=True)
        return jsonify({'share_url': share_url})
        
    except Exception as e:
        logging.error(f"Error generating share link for {chat_id}: {e}")
        return jsonify({'error': 'Error generating share link'}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
