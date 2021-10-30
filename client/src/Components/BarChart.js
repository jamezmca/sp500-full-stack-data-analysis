import React from 'react'
import { Bar } from 'react-chartjs-2';

export default function BarChart({data}) {
    let risky = data.getRiskReward

    console.log('risky', risky)
    const labels = risky.map(label => label.name.replace('_', ' ').toLowerCase()).slice(0,15)
    const risk = risky.map(label => label.risk).slice(0,15)
    const reward = risky.map(label => label.reward).slice(0,15)
    return (
        <Bar
            data={{
                labels: labels,
                datasets: [
                    {
                        label: 'Average Successful Regonition Per Class',
                        data: reward,
                        backgroundColor: [
                            'rgba(255, 99, 132, 0.2)',
                            'rgba(54, 162, 235, 0.2)',
                            'rgba(255, 206, 86, 0.2)',
                            'rgba(75, 192, 192, 0.2)',
                            'rgba(153, 102, 255, 0.2)',
                            'rgba(255, 159, 64, 0.2)'
                        ],
                        borderColor: [
                            'rgba(255,99,132,1)',
                            'rgba(54, 162, 235, 1)',
                            'rgba(255, 206, 86, 1)',
                            'rgba(75, 192, 192, 1)',
                            'rgba(153, 102, 255, 1)',
                            'rgba(255, 159, 64, 1)'
                        ],
                        borderWidth: 1,
                    }
                ]
            }}
            height={400}
            width={600}

        />
    )
}
