
(async () => {
    // Fetch the topology for Ghana
    const topology = await fetch(
        'https://code.highcharts.com/mapdata/countries/gh/gh-all.topo.json'
    ).then(response => response.json());

    // Prepare a dummy data array to populate the map
    const data = [
        ['gh-ah', 10], ['gh-ep', 11], ['gh-wp', 12], ['gh-aa', 13],
        ['gh-tv', 14], ['gh-np', 15], ['gh-ue', 16], ['gh-uw', 17],
        ['gh-ba', 18], ['gh-cp', 19]
    ];

    // Create the map
    const chart = Highcharts.mapChart('container', {
        chart: {
            map: topology
        },

        title: {
            text: 'Highcharts Maps Ghana'
        },

        subtitle: {
            text: 'Extracting hc-key and region names'
        },

        mapNavigation: {
            enabled: true,
            buttonOptions: {
                verticalAlign: 'bottom'
            }
        },

        colorAxis: {
            min: 0
        },

        series: [{
            data: data,
            name: 'Random data',
            states: {
                hover: {
                    color: '#BADA55'
                }
            },
            dataLabels: {
                enabled: true,
                format: '{point.name}'
            }
        }]
    });

    // Log the hc-key and name pairs to the console
    chart.series[0].data.forEach(dataPoint => {
        console.log("${dataPoint['hc-key']}", "${dataPoint.name}");
    });
})();
this is the javascript code for mapping in ghana, if you are mapping , the last lines are important, copy and paste those in a demo version.