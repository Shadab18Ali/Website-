const MAX_BODY_BYTES = 12000;
// Must match the options on contact.html (see tools/build_pages.py).
const SERVICES = new Set([
  'Shopify',
  'WordPress / WooCommerce',
  'Website Redesign',
  'Custom Development',
  'Other',
]);
const BUDGETS = new Set([
  'Under ₹25,000',
  '₹25,000–₹50,000',
  '₹50,000–₹1,00,000',
  '₹1,00,000+',
  'Not sure yet',
]);
const TIMELINES = new Set([
  'ASAP',
  '2–4 weeks',
  '1–2 months',
  'Flexible',
]);

function result(message, status) {
  return Response.json({ message }, {
    status,
    headers: { 'Cache-Control': 'no-store' },
  });
}

function field(form, name, maxLength) {
  const value = String(form.get(name) ?? '').trim();
  return value.length <= maxLength ? value : null;
}

export async function POST(request) {
  const contentType = request.headers.get('content-type') ?? '';
  if (!contentType.startsWith('application/x-www-form-urlencoded')) {
    return result('Unsupported form format.', 415);
  }
  if (Number(request.headers.get('content-length') ?? 0) > MAX_BODY_BYTES) {
    return result('Your message is too long.', 413);
  }

  let form;
  try {
    const body = await request.text();
    if (new TextEncoder().encode(body).length > MAX_BODY_BYTES) {
      return result('Your message is too long.', 413);
    }
    form = new URLSearchParams(body);
  } catch {
    return result('Could not read the form.', 400);
  }

  // Quietly accept the hidden field so simple bots do not trigger email.
  if (form.get('bot-field')) return result('Your request was received.', 200);

  const name = field(form, 'name', 100);
  const email = field(form, 'email', 200);
  const service = field(form, 'service', 100);
  const website = field(form, 'website', 250);
  const details = field(form, 'details', 3000);
  const budget = field(form, 'budget', 60);
  const timeline = field(form, 'timeline', 60);
  const validEmail = email && /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  const validWebsite = !website || /^https?:\/\/[^\s.]+\.[^\s]+$/i.test(website);
  const validBudget = !budget || BUDGETS.has(budget);
  const validTimeline = !timeline || TIMELINES.has(timeline);
  if (!name || !validEmail || !SERVICES.has(service) || !validWebsite || !details || !validBudget || !validTimeline) {
    return result('Please complete the required fields with valid details.', 400);
  }

  const { RESEND_API_KEY, CONTACT_TO_EMAIL, CONTACT_FROM_EMAIL } = process.env;
  if (!RESEND_API_KEY || !CONTACT_TO_EMAIL || !CONTACT_FROM_EMAIL) {
    console.error('Contact form email settings are missing.');
    return result('The form could not send your request. Please email me directly.', 503);
  }

  const text = [
    'New website inquiry',
    '',
    `Name: ${name}`,
    `Email: ${email}`,
    `Project type: ${service}`,
    `Website: ${website || 'Not provided'}`,
    `Budget: ${budget || 'Not specified'}`,
    `Timeline: ${timeline || 'Not specified'}`,
    '',
    'Project details:',
    details,
  ].join('\n');

  try {
    const response = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${RESEND_API_KEY}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        from: CONTACT_FROM_EMAIL,
        to: [CONTACT_TO_EMAIL],
        reply_to: email,
        subject: `Website inquiry: ${service} — ${name}`,
        text,
      }),
    });
    if (!response.ok) {
      console.error('Email provider rejected contact request:', response.status);
      return result('The form could not send. Please email me directly.', 502);
    }
    return result('Your project request was sent.', 200);
  } catch (error) {
    console.error('Contact request failed:', error);
    return result('The form could not send. Please email me directly.', 502);
  }
}
