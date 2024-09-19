import type { NextApiRequest, NextApiResponse } from 'next';

type Event = {
  event_name: string;
  x_position: number;
  y_position: number;
};

type UniquePositions = {
  [key: string]: string[];
};

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method === 'POST') {
    try {
      const data: string[] = req.body;

      if (!Array.isArray(data)) {
        return res.status(400).json({ error: 'Invalid data format' });
      }

      const events = parseEvents(data);

      const uniquePositions: UniquePositions = {
        mousemove: getUniquePositions(events, 'mousemove'),
        mousedown: getUniquePositions(events, 'mousedown'),
        mouseover: getUniquePositions(events, 'mouseover'),
        mouseout: getUniquePositions(events, 'mouseout'),
        mouseup: getUniquePositions(events, 'mouseup')
      };

      const totalUniquePositions = Object.values(uniquePositions).reduce(
        (acc, positions) => acc + positions.length,
        0
      );

      if (totalUniquePositions < 50) {
        return res.status(200).json({ status: 'bot' });
      } else {
        return res.status(200).json({ status: 'user' });
      }
    } catch (error) {
      console.error(error);
      return res.status(500).json({ error: 'Internal server error' });
    }
  } else {
    return res.status(405).json({ error: 'Method not allowed' });
  }
}

function parseEvents(data: string[]): Event[] {
  return data.map((line: string) => {
    const [event_name, , x_position, y_position] = line.split(',');
    return {
      event_name: event_name.trim(),
      x_position: parseInt(x_position.trim(), 10),
      y_position: parseInt(y_position.trim(), 10)
    };
  });
}

function getUniquePositions(events: Event[], eventType: string): string[] {
  const positions = new Set<string>();
  events.forEach((event) => {
    if (event.event_name === eventType) {
      const position = `${event.x_position},${event.y_position}`;
      positions.add(position);
    }
  });
  return Array.from(positions);
}
