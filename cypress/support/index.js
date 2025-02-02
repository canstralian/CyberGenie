Cypress.Commands.add('login', (email, password) => {
  cy.visit('/login');
  cy.get('input[name=email]').type(email);
  cy.get('input[name=password]').type(password);
  cy.get('button[type=submit]').click();
});

Cypress.Commands.add('register', (username, email, password) => {
  cy.visit('/register');
  cy.get('input[name=username]').type(username);
  cy.get('input[name=email]').type(email);
  cy.get('input[name=password]').type(password);
  cy.get('button[type=submit]').click();
});

Cypress.Commands.add('startScan', (targetUrl) => {
  cy.visit('/scans/new');
  cy.get('input[name=target_url]').type(targetUrl);
  cy.get('button[type=submit]').click();
});
