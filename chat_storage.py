import os
import json
import logging
from datetime import datetime
from replit import db

class ChatStorage:
    """Handle chat storage operations using Replit DB"""
    
    def __init__(self):
        self.db = db
        
    def save_chat(self, chat_id, title, content):
        """Save a chat conversation to storage"""
        try:
            chat_data = {
                'id': chat_id,
                'title': title,
                'content': content,
                'created_at': datetime.now().isoformat(),
                'file_format': 'txt'
            }
            
            # Store in Replit DB with chat_id as key
            self.db[f"chat_{chat_id}"] = json.dumps(chat_data)
            
            # Also maintain an index of all chats
            self._update_chat_index(chat_id, title, chat_data['created_at'])
            
            logging.info(f"Chat {chat_id} saved successfully")
            return True
            
        except Exception as e:
            logging.error(f"Error saving chat {chat_id}: {e}")
            return False
    
    def get_chat(self, chat_id):
        """Retrieve a specific chat by ID"""
        try:
            chat_key = f"chat_{chat_id}"
            if chat_key in self.db:
                chat_data = json.loads(self.db[chat_key])
                return chat_data
            return None
            
        except Exception as e:
            logging.error(f"Error retrieving chat {chat_id}: {e}")
            return None
    
    def get_all_chats(self):
        """Get list of all saved chats"""
        try:
            if "chat_index" in self.db:
                chat_index = json.loads(self.db["chat_index"])
                # Sort by creation date (newest first)
                sorted_chats = sorted(
                    chat_index, 
                    key=lambda x: x['created_at'], 
                    reverse=True
                )
                return sorted_chats
            return []
            
        except Exception as e:
            logging.error(f"Error retrieving chat list: {e}")
            return []
    
    def delete_chat(self, chat_id):
        """Delete a chat conversation"""
        try:
            chat_key = f"chat_{chat_id}"
            
            if chat_key in self.db:
                # Remove from storage
                del self.db[chat_key]
                
                # Remove from index
                self._remove_from_chat_index(chat_id)
                
                logging.info(f"Chat {chat_id} deleted successfully")
                return True
            
            return False
            
        except Exception as e:
            logging.error(f"Error deleting chat {chat_id}: {e}")
            return False
    
    def _update_chat_index(self, chat_id, title, created_at):
        """Update the chat index with new chat info"""
        try:
            if "chat_index" in self.db:
                chat_index = json.loads(self.db["chat_index"])
            else:
                chat_index = []
            
            # Add new chat to index
            chat_info = {
                'id': chat_id,
                'title': title,
                'created_at': created_at
            }
            
            # Remove existing entry if it exists (for updates)
            chat_index = [chat for chat in chat_index if chat['id'] != chat_id]
            chat_index.append(chat_info)
            
            self.db["chat_index"] = json.dumps(chat_index)
            
        except Exception as e:
            logging.error(f"Error updating chat index: {e}")
    
    def _remove_from_chat_index(self, chat_id):
        """Remove a chat from the index"""
        try:
            if "chat_index" in self.db:
                chat_index = json.loads(self.db["chat_index"])
                chat_index = [chat for chat in chat_index if chat['id'] != chat_id]
                self.db["chat_index"] = json.dumps(chat_index)
                
        except Exception as e:
            logging.error(f"Error removing from chat index: {e}")
