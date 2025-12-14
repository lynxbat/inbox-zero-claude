# Email Folder Sorting Rules

**Created:** YYYY-MM-DD
**Updated:** YYYY-MM-DD

## Vendor Classification

### Engineering Partners (Development Services)
*Companies providing engineering/development resources*

| Vendor | Domain | Description | Folder |
|--------|--------|-------------|--------|
| **Acme Dev** | acmedev.io | Mobile development partner | Engineering/AcmeDev |
| **TechPartner** | techpartner.com | Backend services | Engineering/TechPartner |

### Ecommerce Platforms
*Systems you run commerce on*

| Vendor | Domain | Description | Folder |
|--------|--------|-------------|--------|
| **Shopify** | shopify.com | Ecommerce platform | Ecommerce/Platforms/Shopify |
| **BigCommerce** | bigcommerce.com | Ecommerce platform | Ecommerce/Platforms/BigCommerce |
| **WooCommerce** | woocommerce.com | WordPress ecommerce | Ecommerce/Platforms/WooCommerce |

### Ecommerce Vendors
*Vendors providing ecommerce services*

| Vendor | Domain | Description | Folder |
|--------|--------|-------------|--------|
| **Agency One** | agencyone.com | Implementation partner | Ecommerce/Vendors/AgencyOne |
| **MarketplaceCo** | marketplaceco.com | Marketplace management | Ecommerce/Vendors/MarketplaceCo |

### Payments
*Payment processing vendors*

| Vendor | Domain | Description | Folder |
|--------|--------|-------------|--------|
| **Stripe** | stripe.com | Payment processing | Payments/Stripe |
| **PayPal** | paypal.com | Payment processing | Payments/PayPal |
| **Square** | square.com | POS and payments | Payments/Square |

### Supply Chain
*Order management, warehouse, fulfillment*

| Vendor | Domain | Description | Folder |
|--------|--------|-------------|--------|
| **ShipCo** | shipco.com | Order Management System | Supply Chain/OMS/ShipCo |
| **WarehousePro** | warehousepro.com | WMS provider | Supply Chain/WMS/WarehousePro |

### Cloud Infrastructure
*Cloud and infrastructure providers*

| Vendor | Domain | Description | Folder |
|--------|--------|-------------|--------|
| **AWS** | amazon.com | Amazon cloud | Cloud/AWS |
| **Google Cloud** | google.com | Google cloud | Cloud/Google |
| **Azure** | microsoft.com | Microsoft cloud | Cloud/Azure |

### Consulting (Strategy)
*Strategy and management consulting*

| Vendor | Domain | Description | Folder |
|--------|--------|-------------|--------|
| **StratCo** | stratco.com | Strategy consulting | Consulting/StratCo |
| **TechAdvisors** | techadvisors.com | IT consulting | Consulting/TechAdvisors |

### Security & Observability
*Security and monitoring vendors*

| Vendor | Domain | Description | Folder |
|--------|--------|-------------|--------|
| **SecureCo** | secureco.com | Security services | Security/SecureCo |
| **MonitorApp** | monitorapp.com | Observability platform | Observability/MonitorApp |

---

## Sender-Based Rules

### Auto-File Rules

| Sender | Subject Pattern | Target Folder |
|--------|-----------------|---------------|
| reports@company.com | "Daily Sales Report" | Analytics/Daily Sales |
| alerts@monitoring.com | * | Incidents |
| *@stripe.com | * | Payments/Stripe |
| *@github.com | * | Engineering |
| *@agencyone.com | * | Ecommerce/Vendors/AgencyOne |
| noreply@company.com | "Weekly Digest" | Analytics/Weekly |

### VIP Senders (Always Review)

- ceo@company.com (CEO)
- manager@company.com (Direct manager)
- vp-product@company.com (VP Product)

---

## Content-Based Rules

### Keywords → Folders

| Keywords in Subject | Target Folder |
|---------------------|---------------|
| "Invoice", "Payment" | Corporate/Finance |
| "Contract", "SOW", "Agreement" | Corporate/Legal |
| "Incident", "Outage", "P1", "P2" | Incidents |
| "Budget", "Forecast", "Capex" | Corporate/Budget |
| "PO", "Purchase Order" | Corporate/Finance |
| "OMS", "Order Management" | Supply Chain/OMS |

### Auto-Archive (Noise)

| Pattern | Reason |
|---------|--------|
| "Out of Office", "Automatic reply" | Routine |
| *@newsletter.* | Marketing noise |
| *@notifications.* | Automated notifications |
| "Unsubscribe" in body | Marketing |

---

## Folder Structure

```
📁 Ecommerce/
   📁 Platforms/
      Shopify/
      BigCommerce/
   📁 Vendors/
      AgencyOne/
      MarketplaceCo/

📁 Engineering/
   AcmeDev/
   TechPartner/

📁 Payments/
   Stripe/
   PayPal/
   Square/

📁 Supply Chain/
   📁 OMS/
   📁 WMS/
   📁 Fulfillment/

📁 Cloud/
   AWS/
   Google/
   Azure/

📁 Security/
📁 Observability/
📁 Consulting/

📁 Corporate/
   📁 Finance/
   📁 Legal/
   📁 Budget/
   📁 HR/

📁 Programs/
   (Cross-cutting initiatives)

📁 Analytics/
   Daily Sales/
   Weekly Reports/

📁 People/
   (Individual 1:1 threads)

📁 Incidents/
   (Historical reference)

📁 Archive/
```
