import flet as ft
import base64
import httpx

def main(page: ft.Page):
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.theme_mode = "light"

    name = ft.TextField(label="Name", width=300, read_only=True)
    designation = ft.TextField(label="Designation", width=300, read_only=True)
    user_id = ft.TextField(label="Enter ID to Search", width=300)
    p_image = ft.Image(width=150, height=150, fit=ft.ImageFit.CONTAIN, border_radius=12)
    status_text = ft.Text()

    def search_user(e):
        search_id = user_id.value.strip()
        if not search_id:
            status_text.value = "Please enter an ID to search."
            page.update()
            return

        # Fetch user data from FastAPI
        try:
            response = httpx.get(f"https://fastapi-3-lohe.onrender.com/search-user/{search_id}")
            if response.status_code == 200:
                data = response.json()
                name.value = data.get("name")
                designation.value = data.get("designation")
                image_base64 = data.get("image_base64")

                # Display the image if available
                if image_base64:
                    p_image.src_base64 = image_base64
                else:
                    p_image.src_base64 = ""

                status_text.value = "User found successfully!"
            else:
                status_text.value = f"Error: {response.json().get('detail', 'Unknown error')}"
                name.value = ""
                designation.value = ""
                p_image.src_base64 = ""

        except Exception as ex:
            status_text.value = f"Error: {ex}"

        page.update()

    search_button = ft.ElevatedButton("Search User", on_click=search_user)

    page.add(user_id, search_button, name, designation, p_image, status_text)

app = ft.app(main, export_asgi_app=True)