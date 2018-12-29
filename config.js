var config = {
    lang: 'zh_cn',
    time: {
        timeFormat: 12,
        displaySeconds: true,
        digitFade: false,
    },
    weather: {
        //change weather params here:
        //units: metric or imperial
        interval: 120000,
        fadeInterval: 10000,
        params: {
            q: 'shanghai',
            units: 'metric',
            // if you want a different lang for the weather that what is set above, change it here
            lang: 'zh_cn',
            APPID: '4757669a2557dd8552e4d1515dca25b7'
        }
    },
    tem_hum: {
      mqttServer: 'mqtt.hellowk.cc',
      mqttServerPort: 9001,
      mqttclientName: "magic_mirror_tem_hum",
      temperatureTopic: 'homekit/himitsu/temperature',
      humidityTopic: 'homekit/himitsu/humidity',
      heatIndexTopic: 'homekit/himitsu/heatIndex'
    },
    compliments: {
        interval: 30000,
        fadeInterval: 4000,
        morning: [
            '早上好!',
            '开始新的一天吧!',
            '睡得怎么样?'
        ],
        afternoon: [
            '下午好',
            '你很棒棒!',
            '你很酷哦!'
        ],
        evening: [
            '早点休息!',
            '你看上去很累了!',
            '晚上好!'
        ]
    },
    calendar: {
        maximumEntries: 10, // Total Maximum Entries
		displaySymbol: true,
		defaultSymbol: 'calendar', // Fontawsome Symbol see http://fontawesome.io/cheatsheet/
        urls: [
		{
			symbol: 'calendar-plus-o',
			url: ''
		},
		// {
		// 	symbol: 'soccer-ball-o',
		// 	url: 'https://www.google.com/calendar/ical/akvbisn5iha43idv0ktdalnor4%40group.calendar.google.com/public/basic.ics',
		// },
		// {
			// symbol: 'mars',
			// url: "https://server/url/to/his.ics",
		// },
		// {
			// symbol: 'venus',
			// url: "https://server/url/to/hers.ics",
		// },
		// {
			// symbol: 'venus-mars',
			// url: "https://server/url/to/theirs.ics",
		// },
		]
    },
    news: {
        feed: 'http://feed43.com/1726484643045386.xml'
    }
}

