import { NextResponse } from 'next/server';
export async function POST(req, res) {
  try {
    const data = await req.json(); 
    console.log("data coming",data)
    if (!Array.isArray(data)) {
      return NextResponse.json({ error: 'Invalid data format' });
    }

    const uniquePositions = {
      mousemove: getUniquePositions(data, 'mousemove'),
      mousedown: getUniquePositions(data, 'mousedown'),
      mouseover: getUniquePositions(data, 'mouseover'),
      mouseout: getUniquePositions(data, 'mouseout'),
      mouseup: getUniquePositions(data, 'mouseup'),
    };

    const totalUniquePositions = Object.values(uniquePositions).reduce(
      (acc, positions) => acc + positions.length,
      0
    );

    if (totalUniquePositions < 300) {
      console.log("bot activity detected")
      return NextResponse.json({ status: 'bot' });
    } else {
      console.log("user activity detected")
      return NextResponse.json({ status: 'user' });
    }
  } catch (error) {
    console.error(error);
    return NextResponse.json({ error: 'Internal server error' });
  }
}

function getUniquePositions(events, eventType) {
  const positions = new Set();
  events.forEach((event) => {
    if (event.eventType === eventType) {
      const position = `${event.x},${event.y}`;
      positions.add(position);
    }
  });
  return Array.from(positions);
}

