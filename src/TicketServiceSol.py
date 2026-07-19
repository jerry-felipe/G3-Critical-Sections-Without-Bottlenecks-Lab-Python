import threading
import time


class TicketService:
    def __init__(self):
        self.available_tickets = 5
        self.lock = threading.Lock()

    def buy_ticket(self, customer):
        # Trabajo lento fuera del lock.
        # No modifica el recurso compartido.
        print(f"{customer} está generando comprobante...")
        time.sleep(0.3)

        # Solo esta sección necesita exclusión mutua.
        with self.lock:
            if self.available_tickets > 0:
                self.available_tickets -= 1
                print(f"{customer} compró ticket. Restan: {self.available_tickets}")
                return True

            print(f"{customer} no pudo comprar. No quedan tickets.")
            return False

    def get_available_tickets(self):
        with self.lock:
            return self.available_tickets


def main():
    service = TicketService()
    start = time.time()

    threads = []

    for i in range(10):
        customer = f"Cliente-{i + 1}"
        thread = threading.Thread(
            target=service.buy_ticket,
            args=(customer,)
        )
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    end = time.time()

    print(f"Tickets finales: {service.get_available_tickets()}")
    print(f"Tiempo total aproximado: {(end - start):.2f} segundos")


if __name__ == "__main__":
    main()
