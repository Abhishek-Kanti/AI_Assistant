css = '''
<style>
.chat-message {
    padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
}
.chat-message.user {
    background-color: #2b313e
}
.chat-message.bot {
    background-color: #475063
}
.chat-message .avatar {
  width: 20%;
}
.chat-message .avatar img {
  max-width: 78px;
  max-height: 78px;
  border-radius: 50%;
  object-fit: cover;
}
.chat-message .message {
  width: 80%;
  padding: 0 1.5rem;
  color: #fff;
}

.stTextInput > div {
    position: sticky;
    top: 0;
    z-index: 1;
    background-color: white;
    border: 1px solid white; /* Add white border */
    border-radius: 10px; /* Add border-radius for curvature */
}

 .circle-image {
    position: absolute;
    top: 50%;
    right: 1;
    transform: translate(0%, -50%);
    border-radius: 50%;
    overflow: hidden;
}

.circle-image img {
    width: 50px;  # Set the desired width
    height: 50px;  # Set the desired height
    top: 50%;
    object-fit: cover;
    border-radius: 50%;
}

.beginning-background {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 68vh;
    background-color: #272731;  /* Set your desired background color */
    border-radius: 15px;  /* Set your desired border-radius for rounded edges */
    padding: 20px;  /* Set your desired padding */
    margin-bottom: 15px;
}

.logo {
    width: 100px;  /* Set your desired width for the logo */
    height: auto;  /* Maintain aspect ratio */
    margin-bottom: 5px;  /* Set margin as needed */
}

.sidebar-button {
    width: 100%;  /* Set width to 100% for full length */
}

h2 {
    color: #FEFDFF;  /* Set your desired color for the text */
    margin-top: 80px;  /* Set margin-top as needed */
}

</style>
'''

bot_Template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://i.ibb.co/x36DfwK/bot-avatar.jpg" style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit: cover;">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_Template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://i.ibb.co/xDY79Xq/user-image.jpg">
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''