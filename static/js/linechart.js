 google.charts.load('current', {'packages':['corechart']});
      google.charts.setOnLoadCallback(drawChart);

      function drawChart() {
        var data = google.visualization.arrayToDataTable([
          ['Year', "World", "United Kingdom", "You"],
          ['2005',  1000,      100,     900],
          ['2010',  2000,      600,     3000],
          ['2015',  1500,      300,     4000],
          ['2021',  800,      1000,     5000],
        ]);

        var options = {
          title: 'Carbon Emission',
        };

        var chart = new google.visualization.LineChart(document.getElementById('chart_div'));

        chart.draw(data, options);
      }