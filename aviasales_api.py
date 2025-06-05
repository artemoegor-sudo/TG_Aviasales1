import requests
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional


class AviasalesAPI:
    """
    A class to interact with Aviasales API for fetching flight information.
    """
    
    def __init__(self, api_token: str):
        self.api_token = api_token
        self.base_url = "https://api.travelpayouts.com"
        self.headers = {
            'X-Access-Token': api_token,
            'Accept-Encoding': 'gzip, deflate'
        }
    
    def get_cheapest_tickets(self, origin: str = "LED", destination: str = "KGD", 
                           currency: str = "RUB", limit: int = 10) -> Optional[List[Dict]]:
        """
        Get cheapest tickets from origin to destination.
        
        Args:
            origin: Origin airport code (default: LED - Saint Petersburg)
            destination: Destination airport code (default: KGD - Kaliningrad)
            currency: Currency for prices (default: RUB)
            limit: Number of results to return
            
        Returns:
            List of flight data or None if error
        """
        try:
            url = f"{self.base_url}/v1/prices/cheap"
            params = {
                'origin': origin,
                'destination': destination,
                'currency': currency
            }
            
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('success') and data.get('data'):
                # Extract flight information
                flights = []
                destination_data = data['data'].get(destination, {})
                
                for key, flight_info in destination_data.items():
                    if isinstance(flight_info, dict):
                        flights.append({
                            'price': flight_info.get('price'),
                            'airline': flight_info.get('airline'),
                            'flight_number': flight_info.get('flight_number'),
                            'departure_at': flight_info.get('departure_at'),
                            'return_at': flight_info.get('return_at'),
                            'expires_at': flight_info.get('expires_at')
                        })
                
                # Sort by price and return limited results
                flights.sort(key=lambda x: x['price'] if x['price'] else float('inf'))
                return flights[:limit]
            
            return None
            
        except requests.exceptions.RequestException as e:
            print(f"API request error: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None
    
    def get_direct_flights(self, origin: str = "LED", destination: str = "KGD", 
                          currency: str = "RUB") -> Optional[List[Dict]]:
        """
        Get direct flights from origin to destination.
        
        Args:
            origin: Origin airport code (default: LED - Saint Petersburg)
            destination: Destination airport code (default: KGD - Kaliningrad)
            currency: Currency for prices
            
        Returns:
            List of direct flight data or None if error
        """
        try:
            url = f"{self.base_url}/v1/prices/direct"
            params = {
                'origin': origin,
                'destination': destination,
                'currency': currency
            }
            
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('success') and data.get('data'):
                flights = []
                destination_data = data['data'].get(destination, {})
                
                for key, flight_info in destination_data.items():
                    if isinstance(flight_info, dict):
                        flights.append({
                            'price': flight_info.get('price'),
                            'airline': flight_info.get('airline'),
                            'flight_number': flight_info.get('flight_number'),
                            'departure_at': flight_info.get('departure_at'),
                            'return_at': flight_info.get('return_at'),
                            'expires_at': flight_info.get('expires_at')
                        })
                
                flights.sort(key=lambda x: x['price'] if x['price'] else float('inf'))
                return flights
            
            return None
            
        except requests.exceptions.RequestException as e:
            print(f"API request error: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None
    
    def get_monthly_prices(self, origin: str = "LED", destination: str = "KGD", 
                          currency: str = "RUB") -> Optional[List[Dict]]:
        """
        Get monthly price trends for the route.
        
        Args:
            origin: Origin airport code (default: LED - Saint Petersburg)
            destination: Destination airport code (default: KGD - Kaliningrad)
            currency: Currency for prices
            
        Returns:
            List of monthly price data or None if error
        """
        try:
            url = f"{self.base_url}/v1/prices/monthly"
            params = {
                'origin': origin,
                'destination': destination,
                'currency': currency
            }
            
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('success') and data.get('data'):
                monthly_data = []
                for month, flight_info in data['data'].items():
                    monthly_data.append({
                        'month': month,
                        'price': flight_info.get('price'),
                        'airline': flight_info.get('airline'),
                        'flight_number': flight_info.get('flight_number'),
                        'departure_at': flight_info.get('departure_at'),
                        'return_at': flight_info.get('return_at')
                    })
                
                return monthly_data
            
            return None
            
        except requests.exceptions.RequestException as e:
            print(f"API request error: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None
    
    def format_flight_info(self, flight: Dict) -> str:
        """
        Format flight information for display.
        
        Args:
            flight: Flight data dictionary
            
        Returns:
            Formatted flight information string
        """
        if not flight:
            return "Данные о рейсе недоступны"
        
        price = flight.get('price', 'Н/Д')
        airline = flight.get('airline', 'Н/Д')
        flight_number = flight.get('flight_number', 'Н/Д')
        departure = flight.get('departure_at', 'Н/Д')
        return_date = flight.get('return_at', 'Н/Д')
        
        # Format dates if available
        if departure != 'Н/Д' and departure:
            try:
                dep_date = datetime.fromisoformat(departure.replace('Z', '+00:00'))
                departure = dep_date.strftime('%Y-%m-%d %H:%M')
            except:
                pass
        
        if return_date != 'Н/Д' and return_date:
            try:
                ret_date = datetime.fromisoformat(return_date.replace('Z', '+00:00'))
                return_date = ret_date.strftime('%Y-%m-%d %H:%M')
            except:
                pass
        
        formatted = f"✈️ **Рейс {airline} {flight_number}**\n"
        formatted += f"💰 Цена: {price} руб.\n"
        formatted += f"🛫 Вылет: {departure}\n"
        
        if return_date != 'Н/Д':
            formatted += f"🛬 Возврат: {return_date}\n"
        
        return formatted 