import { exec } from 'child_process';
import path from 'path';

export async function GET(req) {
  // Updated path to new bot_attacks location
  const scriptPath = path.resolve("bot_attacks", "advanced", "form_bot.py");

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
