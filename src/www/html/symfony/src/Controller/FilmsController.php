<?php

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;
use App\Repository\FilmsRepository;
use Symfony\Component\HttpFoundation\JsonResponse;

class FilmsController extends AbstractController
{
   #[Route('/benchmarking/api')]
   public function list(FilmsRepository $filmsRepository): JsonResponse
   {
       $films = $filmsRepository->findAll();
       $data = [];

       foreach ($films as $film) {
           $data[] = [
               'film_id' => $film->getId(),
               'title' => $film->getTitle(),
               'description' => $film->getDescription(),
               'release_year' => $film->getReleaseYear(),
               'rental_duration' => $film->getRentalDuration(),
               'rental_rate' => $film->getRentalRate(),
               'length' => $film->getLength(),
               'replacement_cost' => $film->getReplacementCost(),
               'rating' => $film->getRating(),
               'special_features' => $film->getSpecialFeatures(),
               'last_update' => $film->getLastUpdate()
           ];
       }

       return new JsonResponse($data, Response::HTTP_OK);
   }
}