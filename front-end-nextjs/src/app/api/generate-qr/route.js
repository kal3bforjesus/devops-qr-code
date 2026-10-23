import { NextResponse } from 'next/server';

export async function POST(request) {
  try {
    const body = await request.json();
    
    // MAGIC: 'api-service' is the internal Kubernetes DNS name! 
    // No public IP needed. This only works inside the cluster.
    const backendRes = await fetch('http://api-service:8000/generate-qr/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    
    const data = await backendRes.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error("Backend error:", error);
    return NextResponse.json({ error: 'Failed to generate QR' }, { status: 500 });
  }
}