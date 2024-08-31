# Custom Mailer

You can customize your emails using templates using variables

Add 'mail_configuration' in your installed app after installing this package

Then migrate to apply related changes for your project

## OTP Sample:

```
payload = {
    "mail_service": "smtp",
    "email_from": "goshweet@gmail.com",
    "recipient_list": "jasirmj@gmail.com",
    "subject": "Test Mail",
    "html_template": "OTP",
    "variables":{
        "otp":"0786",
        "content":"Hi your otp is",
        "brand": "SolutionizeIT"
    }
}

sendMail(**payload)
```

## HTML OTP Template 
```
<div style="font-family: Helvetica,Arial,sans-serif;min-width:1000px;overflow:auto;line-height:2">
    <div style="margin:50px auto;width:70%;padding:20px 0">
        <div style="border-bottom:1px solid #eee">
            <a href="" style="font-size:2.4em;color: #00466a;text-decoration:none;font-weight:600">{{brand}}</a>
        </div>
        <p style="font-size:1.1em">Hi,</p>
        <p>{{content}}</p>
        <h1
            style="background: #00466a;margin: 0 auto;width: max-content;padding: 0 10px;color: #fff;border-radius: 4px;">
            {{otp}}</h1>
        <p style="font-size:0.9em;">Regards,<br />{{brand}}</p>
        <hr style="border:none;border-top:1px solid #eee" />
        <div style="float:right;padding:8px 0;color:#aaa;font-size:0.8em;line-height:1;font-weight:300">
            <p>{{brand}}</p>
            <!-- <p>1600 Amphitheatre Parkway</p>
            <p>California</p> -->
        </div>
    </div>
</div>
```

## Invoice Sample:

```
payload = {
    "mail_service": "smtp",
    "email_from": "goshweet@gmail.com",
    "recipient_list": "jasirmj@gmail.com",
    "subject": "Test Mail",
    "html_template": "invoice",
    "variables": {
        "company_name": "Your Company",
        "address_line_one": "XYZ 2nd Floor",
        "address_line_two": "123 Street, Washington",
        "customer_name": "John Doe",
        "email": "Email: johndoe@gmail.com",
        "phone": "Phone: 555 555 555 555",
        "invoice_id": "1002658",
        "invoice_date": "2024-08-30",
        "due_date": "2024-08-30",
        "invoice_items": [
            {"name": "Product 1", "description": "Description of product 1",
                "quantity": 2, "price": "$20", "total": 123},
            {"name": "Product 2", "description": "Description of product 2",
                "quantity": 1, "price": "$15", "total": 123},
            # Add more items as needed
        ],
        "discount": "10",
        "total_amount": "1055",
    }
}
```

## HTML Invoice Template

```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Invoice</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f8f8f8;
        }
        .invoice-box {
            max-width: 800px;
            margin: auto;
            padding: 30px;
            border: 1px solid #eee;
            background-color: #fff;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.15);
        }
        .invoice-header {
            width: 100%;
            margin-bottom: 20px;
        }
        .invoice-header td {
            vertical-align: top;
        }
        .invoice-header .company-details {
            text-align: right;
        }
        .invoice-header .company-details h2 {
            margin: 0;
            font-size: 18px;
        }
        .invoice-header .company-details p {
            margin: 2px 0;
        }
        .invoice-details {
            margin-bottom: 20px;
        }
        .invoice-details table {
            width: 100%;
            border-collapse: collapse;
        }
        .invoice-details table th, .invoice-details table td {
            padding: 10px;
            text-align: left;
            border-bottom: 1px solid #eee;
        }
        .invoice-details table th {
            background-color: #f2f2f2;
        }
        .invoice-total {
            text-align: right;
            margin-top: 20px;
        }
        .invoice-total h3 {
            margin: 0;
            font-size: 18px;
        }
    </style>
</head>
<body>
    <div class="invoice-box">
        <table class="invoice-header">
            <tr>
                <td>
                    <h1>Invoice</h1>
                </td>
                <td class="company-details">
                    <h2>{{company_name}}</h2>
                    <p>{{address_line_one}}</p>
                    <p>{{address_line_two}}</p>
                    <p>{{email}}</p>
                    <p>{{phone}}</p>
                </td>
            </tr>
        </table>
        <div class="invoice-details">
            <table>
                <tr>
                    <th>Invoice #:</th>
                    <td>{{invoice_id}}</td>
                    <th>Invoice Date:</th>
                    <td>{{invoice_date}}</td>
                </tr>
                <tr>
                    <th>Client Name:</th>
                    <td>{{customer_name}}</td>
                    <th>Due Date:</th>
                    <td>{{due_date}}</td>
                </tr>
            </table>
        </div>
        <div class="invoice-details">
            <table>
                <tr>
                    <th>Description</th>
                    <th>Quantity</th>
                    <th>Unit Price</th>
                    <th>Total</th>
                </tr>
              {% for item in invoice_items %}
                <tr>
                    <td>{{item.name}}</td>
                    <td>{{item.quantity}}</td>
                    <td>{{item.price}}</td>
                    <td>{{item.total}}</td>
                </tr>
              {% endfor %}
                <tr>
                    <th colspan="3" style="text-align: right;">Discount:</th>
                    <td>{{discount}}</td>
                </tr>
                <tr>
                    <th colspan="3" style="text-align: right;">Total:</th>
                    <td>{{total_amount}}</td>
                </tr>
            </table>
        </div>
        <div class="invoice-total">
            <h3>{{total_amount}}</h3>
        </div>
    </div>
</body>
</html>
```

# Mailing Service Config

```
Name: smtp
Email backend: django.core.mail.backends.smtp.EmailBackend
Email host: smtp.gmail.com
Email port: 587
Email use tls: Yes
Email host user: YOUR_LESS_SECURE_ENABLED_GMAIL
Email host password: YOUR_APP_PASSWORD
```