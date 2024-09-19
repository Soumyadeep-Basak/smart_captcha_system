import { exec } from 'child_process';
import path from 'path';

export async function GET(req) {
  const scriptPath = path.resolve('scripts', 'form_bot.py');

  return new Promise((resolve, reject) => {
    exec(`python ${scriptPath}`, (error, stdout, stderr) => {
      if (error) {
        console.error(`Error executing Selenium script: ${stderr}`);
        reject(new Response(`Error: ${stderr}`, { status: 500 }));
      } else {
        console.log(`Selenium script output: ${stdout}`);
        resolve(new Response('Selenium script executed successfully', { status: 200 }));
      }
    });
  });
}
