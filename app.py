import os
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder='static')

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'mp4', 'mov', 'avi', 'mkv'}
MAX_FILE_SIZE = 20 * 1024 * 1024  # 20MB

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/submit-order', methods=['POST'])
def submit_order():
    try:
        # Get form data
        client_name    = request.form.get('clientName', '')
        client_email   = request.form.get('clientEmail', '')
        ui_style       = request.form.get('uiStyle', '')
        colors_raw     = request.form.get('colors', '[]')
        category       = request.form.get('category', '')
        media_option   = request.form.get('mediaOption', '')
        features       = request.form.get('features', '')
        hosting        = request.form.get('hostingDuration', '')
        domain_name    = request.form.get('domainName', '')
        total_price    = request.form.get('totalPrice', '0')

        try:
            colors = json.loads(colors_raw)
        except Exception:
            colors = []

        # Save uploaded files
        saved_files = []
        for f in request.files.getlist('mediaFiles'):
            if f and allowed_file(f.filename):
                fname = secure_filename(f.filename)
                fpath = os.path.join(UPLOAD_FOLDER, fname)
                f.save(fpath)
                saved_files.append({'name': fname, 'path': fpath})

        # Build email
        domain_display = f"{domain_name}.com" if domain_name else "None"
        colors_display = ', '.join(colors) if colors else 'Developer selects'
        files_list = ''.join(f'<li>{sf["name"]}</li>' for sf in saved_files) or '<li>No files uploaded</li>'

        email_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
  body {{ font-family: Georgia, serif; background: #f7f6f3; margin: 0; padding: 24px; color: #1a1916; }}
  .container {{ max-width: 680px; margin: 0 auto; background: #fff; border: 1px solid #e2dfd8; border-radius: 16px; overflow: hidden; }}
  .header {{ background: #1a1916; padding: 36px 40px; }}
  .header h1 {{ color: #fff; font-size: 26px; margin: 0 0 6px; letter-spacing: -0.5px; }}
  .header p {{ color: #9e9b94; margin: 0; font-size: 14px; font-family: sans-serif; }}
  .body {{ padding: 36px 40px; }}
  .section {{ margin-bottom: 28px; }}
  .section-title {{ font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 2px; color: #9e9b94; font-family: sans-serif; margin-bottom: 14px; padding-bottom: 8px; border-bottom: 1px solid #e2dfd8; }}
  .row {{ display: flex; padding: 10px 0; border-bottom: 1px solid #f0ede8; gap: 16px; }}
  .row:last-child {{ border-bottom: none; }}
  .key {{ font-size: 12px; font-weight: 600; color: #9e9b94; text-transform: uppercase; letter-spacing: 1px; font-family: sans-serif; width: 140px; flex-shrink: 0; padding-top: 2px; }}
  .val {{ font-size: 14px; color: #1a1916; font-family: sans-serif; flex: 1; line-height: 1.5; }}
  .price-box {{ background: #1a1916; border-radius: 12px; padding: 28px; text-align: center; margin-top: 28px; }}
  .price-label {{ font-size: 11px; text-transform: uppercase; letter-spacing: 2px; color: #9e9b94; font-family: sans-serif; margin-bottom: 8px; }}
  .price-amount {{ font-size: 56px; font-weight: 700; color: #fff; font-family: Georgia, serif; letter-spacing: -2px; line-height: 1; }}
  .footer {{ background: #f7f6f3; padding: 20px 40px; text-align: center; font-size: 12px; color: #9e9b94; font-family: sans-serif; border-top: 1px solid #e2dfd8; }}
  ul {{ margin: 0; padding-left: 18px; }} li {{ font-size: 13px; color: #6b6860; font-family: sans-serif; padding: 3px 0; }}
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <h1>🌐 New Website Order</h1>
    <p>ThindWorldWeb — A new client has submitted a request</p>
  </div>
  <div class="body">
    <div class="section">
      <div class="section-title">Client Information</div>
      <div class="row"><div class="key">Name</div><div class="val">{client_name}</div></div>
      <div class="row"><div class="key">Email</div><div class="val">{client_email}</div></div>
    </div>
    <div class="section">
      <div class="section-title">Design Preferences</div>
      <div class="row"><div class="key">UI Style</div><div class="val">{ui_style}</div></div>
      <div class="row"><div class="key">Colors</div><div class="val">{colors_display}</div></div>
      <div class="row"><div class="key">Category</div><div class="val">{category}</div></div>
    </div>
    <div class="section">
      <div class="section-title">Media</div>
      <div class="row"><div class="key">Media Option</div><div class="val">{media_option}</div></div>
      <div class="row"><div class="key">Uploaded Files</div><div class="val"><ul>{files_list}</ul></div></div>
    </div>
    <div class="section">
      <div class="section-title">Features</div>
      <div class="row"><div class="key">Requested</div><div class="val">{features or 'None specified'}</div></div>
    </div>
    <div class="section">
      <div class="section-title">Hosting &amp; Domain</div>
      <div class="row"><div class="key">Hosting</div><div class="val">{hosting}</div></div>
      <div class="row"><div class="key">Domain</div><div class="val">{domain_display}</div></div>
    </div>
    <div class="price-box">
      <div class="price-label">Total Project Cost</div>
      <div class="price-amount">${total_price}</div>
    </div>
  </div>
  <div class="footer">ThindWorldWeb • Custom Web Development • thindworld3d@gmail.com</div>
</div>
</body>
</html>"""

        confirmation_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
  body {{ font-family: Georgia, serif; background: #f7f6f3; margin: 0; padding: 24px; color: #1a1916; }}
  .container {{ max-width: 580px; margin: 0 auto; background: #fff; border: 1px solid #e2dfd8; border-radius: 16px; overflow: hidden; }}
  .header {{ background: #1a1916; padding: 40px; text-align: center; }}
  .header h1 {{ color: #fff; font-size: 28px; margin: 0 0 8px; }}
  .header p {{ color: #9e9b94; margin: 0; font-size: 14px; font-family: sans-serif; }}
  .body {{ padding: 36px 40px; font-family: sans-serif; color: #6b6860; line-height: 1.7; font-size: 15px; }}
  .highlight {{ color: #1a1916; font-weight: 600; }}
  .price {{ font-family: Georgia, serif; font-size: 42px; font-weight: 700; color: #1a1916; text-align: center; margin: 20px 0; letter-spacing: -1px; }}
  .footer {{ background: #f7f6f3; padding: 20px 40px; text-align: center; font-size: 12px; color: #9e9b94; font-family: sans-serif; border-top: 1px solid #e2dfd8; }}
</style>
</head>
<body>
<div class="container">
  <div class="header"><h1>Order Confirmed! 🎉</h1><p>ThindWorldWeb</p></div>
  <div class="body">
    <p>Hi <span class="highlight">{client_name}</span>,</p>
    <p>Thank you for your website order! We've received your request and will get started shortly.</p>
    <p>Your total investment:</p>
    <div class="price">${total_price}</div>
    <p>Your website will be <span class="highlight">ready within 3–4 days</span>. We'll be in touch soon with updates!</p>
    <p>If you have any questions, just reply to this email.</p>
    <p>— The ThindWorldWeb Team</p>
  </div>
  <div class="footer">ThindWorldWeb • Custom Web Development</div>
</div>
</body>
</html>"""

        # Send emails via SMTP
        email_user = os.getenv('EMAIL_USER', '')
        email_pass = os.getenv('EMAIL_PASS', '')
        dev_email  = os.getenv('DEVELOPER_EMAIL', 'thindworld3d@gmail.com')

        def send_email(to, subject, html_body, attachments=None):
            msg = MIMEMultipart('alternative')
            msg['From']    = f"ThindWorldWeb <{email_user}>"
            msg['To']      = to
            msg['Subject'] = subject
            msg['Reply-To'] = client_email
            msg.attach(MIMEText(html_body, 'html'))

            if attachments:
                for att in attachments:
                    with open(att['path'], 'rb') as f:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(f.read())
                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition', f'attachment; filename="{att["name"]}"')
                    msg.attach(part)

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(email_user, email_pass)
                server.sendmail(email_user, to, msg.as_string())

        # Send to developer
        send_email(
            to=dev_email,
            subject=f"🌐 New Website Order from {client_name} — ${total_price}",
            html_body=email_html,
            attachments=saved_files
        )

        # Send confirmation to client
        send_email(
            to=client_email,
            subject="✅ Your Website Order is Confirmed — ThindWorldWeb",
            html_body=confirmation_html
        )

        return jsonify({'success': True, 'message': 'Order submitted successfully!'})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
