import * as Turbo from '@hotwired/turbo';
import { createApp } from "@shopify/app-bridge";
import { getSessionToken } from "@shopify/app-bridge/utilities";
import { TitleBar } from '@shopify/app-bridge/actions';


const SESSION_TOKEN_REFRESH_INTERVAL = 2000; // Request a new token every 2s

async function retrieveToken(app) {
  window.sessionToken = await getSessionToken(app);
}

function keepRetrievingToken(app) {
  setInterval(() => {
    retrieveToken(app);
  }, SESSION_TOKEN_REFRESH_INTERVAL);
}

function redirectThroughTurbolinks(isInitialRedirect = false) {
  const data = JSON.parse(
    document.getElementById('shopify-app-init').textContent,
  );
  var validLoadPath = data && data.loadPath;
  var shouldRedirect = false;

  if (isInitialRedirect) {
    shouldRedirect = validLoadPath;
  }
  if (shouldRedirect) Turbo.visit(data.loadPath);
}

document.documentElement.addEventListener(
  'turbo:before-fetch-request',
  function (event) {
    console.log(event.detail);
    event.detail.fetchOptions.headers['Authorization'] =
      'Bearer ' + window.sessionToken;
  },
);

document.addEventListener('DOMContentLoaded', async () => {
  const data = JSON.parse(
    document.getElementById('shopify-app-init').textContent,
  );
  console.log(data)

  window.app = createApp({
    apiKey: data.apiKey,
    host: data.encodedHost,
    forceRedirect: true,
  });

  TitleBar.create(app, {
    title: data.page,
  });

  // Wait for a session token before trying to load an authenticated page
  await retrieveToken(app);

  // Keep retrieving a session token periodically
  keepRetrievingToken(app);

  // Redirect to the requested page when DOM loads
  var isInitialRedirect = true;
  redirectThroughTurbolinks(isInitialRedirect);

  document.addEventListener('turbo:load', function (event) {
    redirectThroughTurbolinks();
  });
});