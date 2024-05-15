<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

  <xsl:template match="events">
    <html>
      <head>
        <style>
          table {
            border-collapse: collapse;
            width: 100%;
          }
          th, td {
            border: 1px solid black;
            padding: 8px;
            text-align: left;
          }
          th {
            background-color: #f2f2f2;
          }
           /* Header styles */
        .header {
            background-color: #333;
            color: #fff;
            padding: 10px;
            text-align: center;
        }

        .header h1 {
            margin: 0;
            font-size: 24px;
        }

        /* Navigation links */
        .navbar {
            display: flex;
            justify-content: center;
            margin-top: 10px;
        }

        .navbar a {
            color: #fff;
            text-decoration: none;
            margin: 0 10px;
        }

        .navbar a:hover {
            text-decoration: underline;
        }
        </style>
      </head>
      <body>
      <!-- Header -->
    <div class="header">
        <h1>My App</h1>
        <div class="navbar">
            <a href="/">Home</a>
            <a href="/events">View XML</a>
            <a href="/json-events">View JSON</a>
            <a href="/upload">Upload</a>
        </div>
    </div>
        <h2>Events</h2>
        <table>
          <tr>
            <th>ID</th>
            <th>Status</th>
            <th>Date</th>
            <th>Time</th>
            <th>Duration</th>
            <th>Type</th>
            <th>Attendees</th>
            <th>Catering Company</th>
            <th>Client Name</th>
            <th>Phone</th>
            <th>Menu</th>
            <th>Pricing</th>
            <th>Notes</th>
          </tr>
          <xsl:apply-templates select="event"/>
        </table>
      </body>
    </html>
  </xsl:template>

  <xsl:template match="event">
    <tr>
      <td><xsl:value-of select="id"/></td>
      <td><xsl:value-of select="@status"/></td>
      <td><xsl:value-of select="date"/></td>
      <td><xsl:value-of select="time"/></td>
      <td><xsl:value-of select="duration"/></td>
      <td><xsl:value-of select="type"/></td>
      <td><xsl:value-of select="attendees"/></td>
      <td><xsl:value-of select="cateringCompany"/></td>
      <td><xsl:value-of select="clientName"/></td>
      <td><xsl:value-of select="phone"/></td>
      <td>
        <xsl:for-each select="menu/*">
          <xsl:value-of select="concat(dish, ', ')"/>
        </xsl:for-each>
      </td>
      <td><xsl:value-of select="pricing/price"/></td>
      <td><xsl:value-of select="notes"/></td>
    </tr>
  </xsl:template>

</xsl:stylesheet>
