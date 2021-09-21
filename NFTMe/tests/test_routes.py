#### This file of unit tests ensures the functionality of the routes are as expected. ####

# Helper function to log in to the app and authenticate.
def login(client, email, password):
    return client.post(
        "/login",
        data=dict(email=email, password=password, test=True),
        follow_redirects=True,
    )


# Helper function to log out of the app.
def logout(client):
    return client.get("/logout", follow_redirects=True)


# TESTS #
# Tests to see if the layout page displays.
def test_layout(client):
    """
    GIVEN nothing (not authenticated)
    WHEN we go to the "/" endpoint
    THEN check if the layout is displayed.
    """
    results = client.get("/")
    assert b"NFTMe" in results.data


# Tests to see if the about page displays when not authenticated and when authenticated.
def test_about(client):
    """
    GIVEN an unauthenticated and an authenticated user
    WHEN we go to the "/about" endpoint
    THEN check if the about page is displayed.
    """
    username = "test@gmail.com"
    password = "password"

    results = login(client, username, password)
    assert results.status_code == 200

    results = client.get("/about")
    assert b"Shopify" in results.data

    results = logout(client)
    assert results.status_code == 200

    results = client.get("/about")
    assert b"Shopify" in results.data


# Tests to see if the home page displays when authenticated.
def test_home_page(client):
    """
    GIVEN an authenticated user
    WHEN we go to the "/home" endpoint
    THEN check if the home page is displayed.
    """
    login(client, "test@gmail.com", "password")
    results = client.get("/home")
    logout(client)
    assert b"NFT Marketplace" in results.data


# Tests to see if the register page is displayed.
def test_register_page(client):
    """
    GIVEN nothing
    WHEN we go to the "/register" endpoint
    THEN check if the register page is displayed.
    """
    results = client.get("/register")
    logout(client)
    assert b"Join Today" in results.data


# Tests to see if log in and log out succeeds if user is legitimate, and fails if user does not exist.
def test_login_logout(client):
    """
    GIVEN a valid users' credentials
    WHEN we go to the "/login" endpoint, and proceedingly the "/logout" endpoint
    THEN check if the user is successfully logged in and out
    """
    username = "test@gmail.com"
    password = "password"

    results = login(client, username, password)
    assert results.status_code == 200

    results = logout(client)
    assert results.status_code == 200


# Tests to see that the user gets redirected if not authenticated.
def test_account_page_not_authenticated(client):
    """
    GIVEN an unauthenticated user
    WHEN we go to the "/account" endpoint
    THEN ensure the user is redirected
    """
    results = client.get("/account")

    # make sure we are redirected (as the user cannot access this page)
    assert results.status_code == 302


# Tests to see that an authenticated user can access their account page.
def test_account_page_authenticated(client):
    """
    GIVEN an authenticated user
    WHEN we go to the "/account" endpoint
    THEN ensure account page is displayed
    """
    username = "test@gmail.com"
    password = "password"

    results = login(client, username, password)
    assert results.status_code == 200

    results = client.get("/account")

    logout(client)
    assert b"My NFTs" in results.data


# Tests to see that the user gets redirected if not authenticated.
def test_my_nft_page_not_authenticated(client):
    """
    GIVEN an unauthenticated user
    WHEN we go to the "/my_nfts" endpoint
    THEN ensure the user is redirected
    """
    results = client.get("/my_nfts")

    # make sure we are redirected (as the user cannot access this page)
    assert results.status_code == 302


# Tests to see that an authenticated user can access their my_nft page.
def test_my_nft_page_not_authenticated(client):
    """
    GIVEN an authenticated user
    WHEN we go to the "/account" endpoint
    THEN ensure account page is displayed
    """
    username = "test@gmail.com"
    password = "password"

    results = login(client, username, password)
    assert results.status_code == 200

    results = client.get("/my_nfts")

    logout(client)
    assert b"My NFTs" in results.data


# In the future, more tests here...
