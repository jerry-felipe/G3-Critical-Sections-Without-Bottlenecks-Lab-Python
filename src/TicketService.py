import threading
import time


class TicketService:
    def __init__(self):
        self.available_tickets = 5
        self.lock = threading.Lock()

    def buy_ticket(self, customer):
        # PROBLEMA:
        # El lock cubre todo el proceso, incluyendo trabajo lento
        # que no modifica el recurso compartido.
        with self.lock:
            print(f"{customer} está generando comprobante...")

            # Simula una operación lenta que NO necesita lock
            time.sleep(0.3)

            if self.available_tickets > 0:
                self.available_tickets -= 1
                print(f"{customer} compró ticket. Restan: {self.available_tickets}")
                return True

            print(f"{customer} no pudo comprar. No quedan tickets.")
            return False


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

    print(f"Tickets finales: {service.available_tickets}")
    print(f"Tiempo total aproximado: {(end - start):.2f} segundos")


if __name__ == "__main__":
    main()
