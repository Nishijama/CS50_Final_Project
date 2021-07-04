
type="text/javascript"

      // Load Charts and the corechart package.
      google.charts.load('current', {'packages':['corechart']});

      // Draw the pie chart for Sarah's pizza when Charts is loaded.
      google.charts.setOnLoadCallback(drawSarahChart);

      // Draw the pie chart for the Anthony's pizza when Charts is loaded.
      google.charts.setOnLoadCallback(drawAnthonyChart);

      // Callback that draws the pie chart for Sarah's pizza.
      function drawSarahChart() {

        // Create the data table for Sarah's pizza.
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'Topping');
        data.addColumn('number', 'Slices');
        data.addRows([
          ['SPOC', 1],
          ['Reservations', 1],
          ['DT S/M', 2],
          ['DT D/A', 2],
        ]);

        // Set options for Sarah's pie chart.
        var options = {title:'Tasks this month',
                       width:400,
                       height:300,
                       colors: ['#051C2C', '#00A9F4','#1F40E6', '#AAE6F0']
        };

        // Instantiate and draw the chart for Sarah's pizza.
        var chart = new google.visualization.PieChart(document.getElementById('Taskschart'));
        chart.draw(data, options);
      }

      // Callback that draws the pie chart for Anthony's pizza.
      function drawAnthonyChart() {

        // Create the data table for Anthony's pizza.
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'Date');
        data.addColumn('number', 'Requests');
        data.addRows([
                ['1', 2],
                ['2', 2],
                ['3', 2],
                ['4', 0],
                ['5', 3],
                ['6', 2],
                ['7', 2],
                ['8', 2],
                ['9', 0],
                ['10', 3],
                ['11', 2],
                ['12', 2],
                ['13', 2],
                ['14', 0],
                ['15', 3],
                ['16', 2],
                ['17', 2],
                ['18', 2],
                ['19', 0],
                ['20', 3],
                ['21', 2],
                ['22', 2],
                ['23', 2],
                ['24', 0],
                ['25', 3],
                ['26', 2],
                ['27', 2],
                ['28', 2],
                ['29', 0],
                ['30', 3],
                ]);

        // Set options for Anthony's pie chart.
        var options = {width:1000,
                       height:300,
                       colors: ['#051C2C']
        };

        // Instantiate and draw the chart for Anthony's pizza.
        var chart = new google.visualization.ColumnChart(document.getElementById('PRCchart'));
        chart.draw(data, options);
      }