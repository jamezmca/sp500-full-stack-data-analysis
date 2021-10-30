import React from 'react'
import { Bar } from 'react-chartjs-2';

export default function BarChart({ data }) {
    let risky = data.getRiskReward
    let aloha = risky.sort

    console.log('risky', aloha)
    const labels = risky.map(label => label.name.replaceAll('_', ' ')).slice(-15)
    const risk = risky.map(label => label.risk).slice(-15)
    const reward = risky.map(label => label.reward).slice(-15)
    console.log(risk)
    return (
        <Bar
            data={{
                labels: labels,
                datasets: [
                    {
                        label: 'Return',
                        yAxisID: 'A',
                        data: reward,
                        backgroundColor: [
                            'rgba(0, 200, 50, 0.2)',
                            'rgba(54, 162, 235, 0.2)',
                            'rgba(255, 206, 86, 0.2)',
                            'rgba(75, 192, 192, 0.2)',
                            'rgba(153, 102, 255, 0.2)',
                            'rgba(255, 159, 64, 0.2)'
                        ],
                        borderColor: [
                            'rgba(0, 200, 50, 1)',
                            'rgba(54, 162, 235, 1)',
                            'rgba(255, 206, 86, 1)',
                            'rgba(75, 192, 192, 1)',
                            'rgba(153, 102, 255, 1)',
                            'rgba(255, 159, 64, 1)'
                        ],
                        borderWidth: 1,
                    },
                    {
                        label: 'Risk',
                        yAxisID: 'B',
                        data: risk,
                        backgroundColor: [
                            'rgba(255, 99, 132, 0.2)',
                        ],
                        borderColor: [
                            'rgba(255,99,132,1)',
                        ],
                        borderWidth: 1,
                    }

                ],
                options: {
                    scales: {
                        A: {
                            type: 'linear',
                            position: 'left',

                        },
                        B: {
                            type: 'linear',
                            position: 'right',

                        }
                    }
                  }
            }}
            height={400}
            width={600}

        />
    )
}
