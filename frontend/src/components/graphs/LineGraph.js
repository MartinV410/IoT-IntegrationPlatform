import React from 'react';
import { LineChart, AreaChart, Area, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

// const data = [
//   {
//     name: 'Page A',
//     uv: 4000,
//     pv: 2400,
//     amt: 2400,
//   },
//   {
//     name: 'Page B',
//     uv: 3000,
//     pv: 1398,
//     amt: 2210,
//   },
//   {
//     name: 'Page C',
//     uv: 2000,
//     pv: 9800,
//     amt: 2290,
//   },
//   {
//     name: 'Page D',
//     uv: 2780,
//     pv: 3908,
//     amt: 2000,
//   },
//   {
//     name: 'Page E',
//     uv: 1890,
//     pv: 4800,
//     amt: 2181,
//   },
//   {
//     name: 'Page F',
//     uv: 2390,
//     pv: 3800,
//     amt: 2500,
//   },
//   {
//     name: 'Page G',
//     uv: 3490,
//     pv: 4300,
//     amt: 2100,
//   },
// ];

export default function LineGraph({data, dataKey, lines}) {


    return (
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart
          data={data}
          margin={{
            right: 20,
            left: -25,

          }}
        >
          <XAxis dataKey={dataKey} />
          <YAxis />
          <Tooltip />
          {
            lines.map((line) => {
              return (
                  <Area type="monotone" dataKey={line.dataKey} stroke={line.color} fill={line.color} />
              )
            })
          }
          {/*<Line type="monotone" dataKey="pv" stroke="#8884d8" />*/}
          {/*<Line type="monotone" dataKey="uv" stroke="#82ca9d" />*/}
        </AreaChart>
      </ResponsiveContainer>
    )
}