/**
 * LUMÈRA LUXE · Google Apps Script for Real-Time Order & Customer Sync
 * 
 * Instructions:
 * 1. Open Google Sheets (https://sheets.new) and name it "LUMÈRA LUXE Orders & Customer Vault".
 * 2. In the top menu, click Extensions > Apps Script.
 * 3. Delete any default code in Code.gs and replace it with this entire file.
 * 4. Click "Deploy" > "New deployment".
 * 5. Select type: "Web app".
 * 6. Under "Execute as", select "Me (your email)".
 * 7. Under "Who has access", select "Anyone". (CRITICAL: Must be "Anyone" so the website can submit orders).
 * 8. Click "Deploy", authorize permissions, and copy the "Web app URL" (starts with https://script.google.com/macros/s/...).
 * 9. Paste that URL into .env as:
 *    PUBLIC_GOOGLE_SHEET_WEBHOOK_URL="https://script.google.com/macros/s/.../exec"
 *    (or into siteConfig.googleSheetWebhookUrl in src/data/site.ts).
 */

function setupHeadersIfEmpty(sheet) {
  // If run directly from the Apps Script editor, get the active sheet
  if (!sheet) {
    sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  }
  
  if (sheet.getLastRow() === 0) {
    var headers = [
      "Order ID",
      "Date & Time (Qatar)",
      "Customer Name",
      "WhatsApp Mobile",
      "Email Address",
      "Municipality / Area",
      "Street Address / Villa",
      "Order Total (QAR)",
      "Items Count",
      "Items Summary",
      "Delivery Notes",
      "Payment Method",
      "Order Status",
      "Items JSON (Raw Data for Future Store Migration)",
      "Timestamp (ISO)"
    ];
    
    sheet.appendRow(headers);
    
    // Style headers
    var headerRange = sheet.getRange(1, 1, 1, headers.length);
    headerRange.setFontWeight("bold");
    headerRange.setBackground("#2A2421");
    headerRange.setFontColor("#FFFFFF");
    headerRange.setFontFamily("Arial");
    sheet.setFrozenRows(1);
    Logger.log("✅ LUMÈRA LUXE header row created successfully!");
  } else {
    Logger.log("ℹ️ Headers already exist in this sheet.");
  }
}

function doPost(e) {
  try {
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    setupHeadersIfEmpty(sheet);
    
    var data = {};
    if (e && e.postData && e.postData.contents) {
      data = JSON.parse(e.postData.contents);
    }
    
    var row = [
      data.orderRef || "LL-" + new Date().getTime(),
      data.dateQatar || new Date().toLocaleString(),
      data.customerName || "N/A",
      data.phone || "N/A",
      data.email || "N/A",
      data.municipality || "Doha",
      data.streetAddress || "N/A",
      data.totalAmountQar || 0,
      data.totalItemsCount || 1,
      data.itemsSummary || "N/A",
      data.deliveryNotes || "None",
      data.paymentMethod || "Cash / Card on Delivery (POS)",
      "New Order Received",
      data.itemsJson || "[]",
      data.timestamp || new Date().toISOString()
    ];
    
    sheet.appendRow(row);
    
    return ContentService.createTextOutput(JSON.stringify({
      status: "success",
      orderRef: data.orderRef
    })).setMimeType(ContentService.MimeType.JSON);
    
  } catch (err) {
    return ContentService.createTextOutput(JSON.stringify({
      status: "error",
      message: err.toString()
    })).setMimeType(ContentService.MimeType.JSON);
  }
}

function doGet(e) {
  return ContentService.createTextOutput(JSON.stringify({
    status: "online",
    brand: "LUMÈRA LUXE",
    service: "Orders & Customer Sync Webhook",
    timestamp: new Date().toISOString()
  })).setMimeType(ContentService.MimeType.JSON);
}

/**
 * Optional Test Runner:
 * Select "testOrderSync" in the dropdown and click "Run" to test adding a sample order row!
 */
function testOrderSync() {
  var sampleEvent = {
    postData: {
      contents: JSON.stringify({
        orderRef: "LL-TEST01",
        dateQatar: new Date().toLocaleString("en-US", { timeZone: "Asia/Qatar" }),
        customerName: "Test Customer",
        phone: "+974 5512 3456",
        email: "test@lumeraluxe.qa",
        municipality: "Doha",
        streetAddress: "West Bay Tower 1",
        deliveryNotes: "Sample test order from Apps Script editor",
        totalAmountQar: 450,
        totalItemsCount: 1,
        paymentMethod: "Cash / Card on Delivery (POS)",
        itemsSummary: "1x Baccarat Rouge 540 (70ml) - 450 QAR",
        itemsJson: JSON.stringify([{ id: "test", name: "Baccarat Rouge 540", quantity: 1, priceQar: 450 }]),
        timestamp: new Date().toISOString()
      })
    }
  };
  
  var result = doPost(sampleEvent);
  Logger.log("Result: " + result.getContent());
}

